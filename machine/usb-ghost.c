#include <stddef.h>
#include <stdbool.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "usbdrv/usbdrv.h"
#include "pt/pt.h"

#include "timer.h"
#include "keycodes.h"

#define REPORT_ID_KEYBOARD 1
#define REPORT_ID_MOUSE    2
#define REPORT_ID_GAMEPAD  3

#define LIGHT_HIGH_THRES    700
#define LIGHT_LOW_THRES     100

// port b
#define player_3 0
#define player_1 4

#define left 5
#define right 1

// port c
#define player_2 1
#define player_4 5

#define up 0
#define down 4

// มาโครสำหรับจำลองการหน่วงเวลาใน protothread
#define PT_DELAY(pt,ms,tsVar) \
  tsVar = timer_millis(); \
  PT_WAIT_UNTIL(pt, timer_millis()-tsVar >= (ms));

/////////////////////////////////////////////////////////////////////
// USB report descriptor, สร้างขึ้นจาก HID Descriptor Tool ซึ่ง
// ดาวน์โหลดได้จาก
//    http://www.usb.org/developers/hidpage/dt2_4.zip
//
// หรือใช้ HIDEdit ซึ่งให้บริการฟรีผ่านเว็บที่ http://hidedit.org/
//
// *** ไม่แนะนำให้สร้างเองด้วยมือ ***
/////////////////////////////////////////////////////////////////////
PROGMEM const char usbHidReportDescriptor[USB_CFG_HID_REPORT_DESCRIPTOR_LENGTH] = 
{
  ////////////////////////////////////
  // โครงสร้าง HID report สำหรับคียบอร์ด
  ////////////////////////////////////
  0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
  0x09, 0x06,                    // USAGE (Keyboard)
  0xa1, 0x01,                    // COLLECTION (Application)
  0x85, 0x01,                    //   REPORT_ID (1)
  0x05, 0x07,                    //   USAGE_PAGE (Keyboard)
  0x19, 0xe0,                    //   USAGE_MINIMUM (Keyboard LeftControl)
  0x29, 0xe7,                    //   USAGE_MAXIMUM (Keyboard Right GUI)
  0x15, 0x00,                    //   LOGICAL_MINIMUM (0)
  0x25, 0x01,                    //   LOGICAL_MAXIMUM (1)
  0x75, 0x01,                    //   REPORT_SIZE (1)
  0x95, 0x08,                    //   REPORT_COUNT (8)
  0x81, 0x02,                    //   INPUT (Data,Var,Abs)
  0x95, 0x04,                    //   REPORT_COUNT (1) now is 4
  0x75, 0x08,                    //   REPORT_SIZE (8)
  0x25, 0x65,                    //   LOGICAL_MAXIMUM (101)
  0x19, 0x00,                    //   USAGE_MINIMUM (Reserved (no event indicated))
  0x29, 0x65,                    //   USAGE_MAXIMUM (Keyboard Application)
  0x81, 0x00,                    //   INPUT (Data,Ary,Abs)
  0xc0,                          // END_COLLECTION

  //////////////////////////////////////
  // โครงสร้าง HID report สำหรับเมาส์ 3 ปุ่ม
  //////////////////////////////////////
  0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
  0x0b, 0x02, 0x00, 0x01, 0x00,  // USAGE (Generic Desktop:Mouse)
  0xa1, 0x01,                    // COLLECTION (Application)
  0x0b, 0x01, 0x00, 0x01, 0x00,  //   USAGE (Generic Desktop:Pointer)
  0xa1, 0x00,                    //   COLLECTION (Physical)
  0x85, 0x02,                    //     REPORT_ID (2)
  0x05, 0x09,                    //     USAGE_PAGE (Button)
  0x1b, 0x01, 0x00, 0x09, 0x00,  //     USAGE_MINIMUM (Button:Button 1)
  0x2b, 0x03, 0x00, 0x09, 0x00,  //     USAGE_MAXIMUM (Button:Button 3)
  0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
  0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
  0x75, 0x01,                    //     REPORT_SIZE (1)
  0x95, 0x03,                    //     REPORT_COUNT (3)
  0x81, 0x02,                    //     INPUT (Data,Var,Abs)
  0x75, 0x05,                    //     REPORT_SIZE (5)
  0x95, 0x01,                    //     REPORT_COUNT (1)
  0x81, 0x03,                    //     INPUT (Cnst,Var,Abs)
  0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
  0x0b, 0x30, 0x00, 0x01, 0x00,  //     USAGE (Generic Desktop:X)
  0x0b, 0x31, 0x00, 0x01, 0x00,  //     USAGE (Generic Desktop:Y)
  0x15, 0x81,                    //     LOGICAL_MINIMUM (-127)
  0x25, 0x7f,                    //     LOGICAL_MAXIMUM (127)
  0x75, 0x08,                    //     REPORT_SIZE (8)
  0x95, 0x02,                    //     REPORT_COUNT (2)
  0x81, 0x06,                    //     INPUT (Data,Var,Rel)
  0xc0,                          //     END_COLLECTION
  0xc0,                          // END_COLLECTION

  ////////////////////////////////////////////////////////////
  // โครงสร้าง HID report สำหรับเกมแพดแบบหนึ่งปุ่มกดและหนึ่งก้านแอนะล็อก
  ////////////////////////////////////////////////////////////
  0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
  0x09, 0x04,                    // USAGE (Joystick)
  0xa1, 0x01,                    // COLLECTION (Application)
  0x05, 0x01,                    //   USAGE_PAGE (Generic Desktop)
  0x09, 0x01,                    //   USAGE (Pointer)
  0xa1, 0x00,                    //   COLLECTION (Physical)
  0x85, 0x03,                    //     REPORT_ID (3)
  0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
  0x09, 0x32,                    //     USAGE (Z)
  0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
  0x26, 0xff, 0x03,              //     LOGICAL_MAXIMUM (1023)
  0x75, 0x0a,                    //     REPORT_SIZE (10)
  0x95, 0x01,                    //     REPORT_COUNT (1)
  0x81, 0x02,                    //     INPUT (Data,Var,Abs)
  0x05, 0x09,                    //     USAGE_PAGE (Button)
  0x09, 0x01,                    //     USAGE (Button 1)
  0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
  0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
  0x75, 0x01,                    //     REPORT_SIZE (1)
  0x95, 0x01,                    //     REPORT_COUNT (1)
  0x81, 0x02,                    //     INPUT (Data,Var,Abs)
  0x75, 0x01,                    //     REPORT_SIZE (1)
  0x95, 0x05,                    //     REPORT_COUNT (5)
  0x81, 0x03,                    //     INPUT (Cnst,Var,Abs)
  0xc0,                          //   END_COLLECTION
  0xc0                           // END_COLLECTION
};

typedef struct
{
  /* +----\------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |Byte \ Bit |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
   * +------\----+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  0        |               Report ID = 1                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  1        |           Modifiers (shift,ctrl,etc)          |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  2        |                 Key Code #1                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  3        |                 Key Code #2                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  4        |                 Key Code #3                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  5        |                 Key Code #4                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   */
  uint8_t  report_id;
  uint8_t  modifiers;
  uint8_t  key_code[4];
} ReportKeyboard;

typedef struct
{
  /* +----\------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |Byte \ Bit |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
   * +------\----+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  0        |               Report ID = 2                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  1        |              Buttons' statuses                |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  2        |                  Delta X                      |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  3        |                  Delta Y                      |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   */
  uint8_t  report_id;
  uint8_t  buttons;
  int8_t   dx;
  int8_t   dy;
} ReportMouse;

typedef struct
{
  /*
   * +----\------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |Byte \ Bit |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
   * +------\----+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  0        |               Report ID = 3                   |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  1        |                 Light (L)                     |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   * |  2        |            UNUSED           | Btn | Light (H) |
   * +-----------+-----+-----+-----+-----+-----+-----+-----+-----+
   */
  uint8_t  report_id;
  uint16_t light:10;  // ค่าแสง 10 บิต (0-1023)
  uint8_t  button:1;  // ปุ่ม 1 บิต
  uint8_t  unused:5;  // ไม่ใช้ แต่ต้องเติมให้เต็มไบต์
} ReportGamepad;


ReportKeyboard reportKeyboard;
ReportMouse reportMouse;
ReportGamepad reportGamepad;

uint16_t light;  // Updated by Light-Task; to be shared among threads

// Protothread states
struct pt main_pt;
struct pt blink_pt;
struct pt all_switch_pt;
struct pt send_4_key_pt;

uint8_t key_player_1;
uint8_t key_player_2;
uint8_t key_player_3;
uint8_t key_player_4;

void init_peripheral(){
    DDRC = 0b100010;
	DDRB = 0b010001;
	PORTC = 0b111111;
	PORTB = 0b111111;
  	DDRD |= (1<<PD3);
}

////////////////////////////////////////////////////////////////
// Automatically called by usbpoll() when host makes a request
////////////////////////////////////////////////////////////////
usbMsgLen_t usbFunctionSetup(uchar data[8])
{
  return 0;  /* Return nothing to host for now */
}

//////////////////////////////////////////////////////////////
void sendKey(uint8_t keycode[], uint8_t modifiers, int type)
{
    reportKeyboard.key_code[0] = keycode[0];
    reportKeyboard.key_code[1] = keycode[1];
    reportKeyboard.key_code[2] = keycode[2];
    reportKeyboard.key_code[3] = keycode[3];
    reportKeyboard.modifiers = modifiers;
    usbSetInterrupt((uchar*)&reportKeyboard, sizeof(reportKeyboard));
    
}

//////////////////////////////////////////////////////////////
void sendMouse(int8_t dx, int8_t dy, uint8_t buttons)
{
  reportMouse.dx = dx;
  reportMouse.dy = dy;
  reportMouse.buttons = buttons;
  usbSetInterrupt((uchar*)&reportMouse, sizeof(reportMouse));
}

void blink(){
	PORTD ^= (1<<PD3);
}

PT_THREAD(send_4_key_task(struct pt *pt)){
    static uint32_t ts = 0;
    PT_BEGIN(pt);

    for (;;)
    {
        //PT_DELAY(pt,1000,ts);
        PT_WAIT_UNTIL(pt,usbInterruptIsReady());
        reportKeyboard.key_code[0] = key_player_1;
        reportKeyboard.key_code[1] = key_player_2;
        reportKeyboard.key_code[2] = key_player_3;
        reportKeyboard.key_code[3] = key_player_4;
        reportKeyboard.modifiers = 0;
        usbSetInterrupt((uchar*)&reportKeyboard, sizeof(reportKeyboard));
        blink();
        //PT_DELAY(pt,20,ts);
        //PT_WAIT_UNTIL(pt,usbInterruptIsReady());
        //reportKeyboard.key_code[0] = KEY_NONE;
        //reportKeyboard.key_code[1] = KEY_NONE;
        //reportKeyboard.key_code[2] = KEY_NONE;
        //reportKeyboard.key_code[3] = KEY_NONE;
        //reportKeyboard.modifiers = 0;
        //usbSetInterrupt((uchar*)&reportKeyboard, sizeof(reportKeyboard));
        //blink();
    }
    PT_END(pt); 
}

PT_THREAD(all_switch_task(struct pt *pt)){
    static uint32_t ts = 0;
    PT_BEGIN(pt);
    int state = 0;
    for(;;){
		
		// Check for player_01
		PORTB &= ~(1<<player_1);
		if((PINC & (1<<up)) == 0){
//			blink();
/*			sendKey(KEY_W,0,1);
			PT_DELAY(pt, 200, ts);			
			sendKey(KEY_NONE,0,1);
			PT_DELAY(pt, 200, ts); */
         key_player_1 = KEY_W;		
		}
		else if((PINC & (1<<down)) ==0){
//			blink();
/*			sendKey(KEY_S,0,1);
			PT_DELAY(pt, 200, ts);
			sendKey(KEY_NONE,0,1);
			PT_DELAY(pt, 200, ts); */
         key_player_1 = KEY_S;		
		}
		else if((PINB & (1<<left)) ==0){
//			blink();
/*			sendKey(KEY_A,0,1);
			PT_DELAY(pt, 200, ts);
			sendKey(KEY_NONE,0,1);
			PT_DELAY(pt, 200, ts);*/
         key_player_1 = KEY_A;			
		}
		else if((PINB & (1<<right)) ==0){
//			blink();
/*			sendKey(KEY_D,0,1);
			PT_DELAY(pt, 200, ts);
			sendKey(KEY_NONE,0,1);
			PT_DELAY(pt, 200, ts);			*/
         key_player_1 = KEY_D;
		}
      else{
         key_player_1 = KEY_NONE;
      }
		PORTB |= (1<<player_1);
		// Check for player_02
		PORTC &= ~(1<<player_2);
		if((PINC & (1<<up)) == 0){
			blink();
//			sendKey(KEY_UP_ARROW,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_2 = KEY_UP_ARROW;		
		}
		else if((PINC & (1<<down)) ==0){
			blink();
//			sendKey(KEY_DOWN_ARROW,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_2 = KEY_DOWN_ARROW;		
		}
		else if((PINB & (1<<left)) ==0){
			blink();
//			sendKey(KEY_LEFT_ARROW,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_2 = KEY_LEFT_ARROW;		
		}
		else if((PINB & (1<<right)) ==0){
			blink();
//			sendKey(KEY_RIGHT_ARROW,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_2 = KEY_RIGHT_ARROW;		
		}
      else{
         key_player_2 = KEY_NONE;
      }
		PORTC |= (1<<player_2);
		// Check for player_03
		PORTB &= ~(1<<player_3);
		if((PINC & (1<<up)) == 0){
			blink();
//			sendKey(KEY_T,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_3 = KEY_T;
		}
		else if((PINC & (1<<down)) ==0){
			blink();
//			sendKey(KEY_G,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_3 = KEY_G;
		}
		else if((PINB & (1<<left)) ==0){
			blink();
//			sendKey(KEY_F,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_3 = KEY_F;
		}
		else if((PINB & (1<<right)) ==0){
			blink();
//			sendKey(KEY_H,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_3 = KEY_H;
		}
      else{
        key_player_3 = KEY_NONE;
      }
		PORTB |= (1<<player_3);
		// Check for player_04
		PORTC &= ~(1<<player_4);
		if((PINC & (1<<up)) == 0){
			blink();
//			sendKey(KEY_I,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_4 = KEY_I;
		}
		else if((PINC & (1<<down)) ==0){
			blink();
//			sendKey(KEY_K,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_4 = KEY_K;
		}
		else if((PINB & (1<<left)) ==0){
			blink();
//			sendKey(KEY_J,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_4 = KEY_J;
		}
		else if((PINB & (1<<right)) ==0){
			blink();
//			sendKey(KEY_L,0,1);
//			PT_DELAY(pt, 200, ts);
         key_player_4 = KEY_L;
		}
      else{
         key_player_4 = KEY_NONE;
      }
		PORTC |= (1<<player_4);
      PT_YIELD(pt);	
//      PT_YIELD(&send_4_key_pt);
	}
	PT_END(pt);
}


PT_THREAD(blink_task(struct pt *pt))
{
  static uint32_t ts = 0;

  PT_BEGIN(pt);

  DDRD |= (1<<PD3);

  for (;;)
  {
    PT_DELAY(pt,500,ts);
    PORTD |= (1<<PD3);
    PT_DELAY(pt,500,ts);
    PORTD &= ~(1<<PD3);
  }

  PT_END(pt);
}

PT_THREAD(main_task(struct pt *pt))
{
    PT_BEGIN(pt);

//    blink_task(&blink_pt);
    all_switch_task(&all_switch_pt); 
    send_4_key_task(&send_4_key_pt);
    PT_END(pt);
}

int main()
{
  // Initialize peripheral board and timer
  init_peripheral();
  timer_init();

  // Initialize USB subsystem
  usbInit();
  usbDeviceDisconnect();
  _delay_ms(300);
  usbDeviceConnect();
  
  // Initialize USB reports
  reportKeyboard.report_id = REPORT_ID_KEYBOARD;
  reportKeyboard.modifiers = 0;
  reportKeyboard.key_code[0] = KEY_NONE;
  reportKeyboard.key_code[1] = KEY_NONE;
  reportKeyboard.key_code[2] = KEY_NONE;
  reportKeyboard.key_code[3] = KEY_NONE;

  // Initialize tasks
  PT_INIT(&main_pt);
  PT_INIT(&blink_pt);
  PT_INIT(&all_switch_pt);
  PT_INIT(&send_4_key_pt);
  sei();
  for (;;)
  {
    usbPoll();
    main_task(&main_pt);
  }
}
