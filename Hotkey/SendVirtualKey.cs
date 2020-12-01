using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace Hotkey
{
    public class VirtualKey
    {
        [DllImport("user32.dll", EntryPoint = "SendInput")]
        public static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        internal static extern short VkKeyScan(char nVirtKey);//将一个字符翻译成相应的虚拟键码和对于当前键盘的转换状态
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        internal static extern short GetKeyState(int nVirtKey);//函数只有一个参数，即虚拟键码。返回值为SHORT类型，即短整型。
        //GetKeyState函数是用来获取指定的虚拟键码的按键的状态。得到的状态表示按键是按下了还是弹起的，还是状态切换（大小写状态、数字键盘锁状态）

        [StructLayout(LayoutKind.Explicit)]
        public struct INPUT
        {
            [FieldOffset(0)]
            public int type;
            [FieldOffset(4)]
            public KEYBDINPUT ki;
            [FieldOffset(4)]
            public MOUSEINPUT mi;
            [FieldOffset(4)]
            public HARDWAREINPUT hi;
        }
        public struct KEYBDINPUT
        {
            public short wVk;
            public short wScan;
            public uint dwFlags;
            public uint time;
            public IntPtr dwExtraInfo;
        }
        public struct MOUSEINPUT
        {
            public int dx;
            public int dy;
            public int mouseData;
            public int dwFlags;
            public int time;
            public IntPtr dwExtraInfo;
        }
        public struct HARDWAREINPUT
        {
            public int uMsg;
            public short wParamL;
            public short wParamH;
        }

        [Flags]// 输入类型
        public enum InputType
        {
            INPUT_MOUSE = 0,
            INPUT_KEYBOARD = 1,
            INPUT_HARDWARE = 2
        }
        [Flags]// KEYBDINPUT => dwFlags
        public enum KEYEVENTF
        {
            KEYDOWN = 0,
            EXTENDEDKEY = 0x0001,
            KEYUP = 0x0002,
            UNICODE = 0x0004,
            SCANCODE = 0x0008
        }
        private static readonly short SHIFT = 0x2A;
        public struct Key
        {
            public string Character;
            public short AsciiCode;
            public short ScanCode;
            public bool Shift;

            public Key(string _Character, short _AsciiCode, short _ScanCode, bool _Shift)
            {
                this.Character = _Character;
                this.AsciiCode = _AsciiCode;
                this.ScanCode = _ScanCode;
                this.Shift = _Shift;
            }

            public void PushKey()
            {
                // 发送按键
                if (this.Shift)
                {
                    INPUT[] input = new INPUT[4];

                    input[0].type = (int)InputType.INPUT_KEYBOARD;
                    //input[0].ki.wVk = 0;
                    input[0].ki.wScan = SHIFT;
                    input[0].ki.dwFlags = (int)KEYEVENTF.SCANCODE;
                    //input[0].ki.time = 0;
                    input[0].ki.dwExtraInfo = IntPtr.Zero;

                    input[1].type = (int)InputType.INPUT_KEYBOARD;
                    //input[1].ki.wVk = 0;
                    input[1].ki.wScan = this.ScanCode;
                    input[1].ki.dwFlags = (int)KEYEVENTF.SCANCODE;
                    //input[1].ki.time = 0;
                    input[1].ki.dwExtraInfo = IntPtr.Zero;

                    input[2].type = (int)InputType.INPUT_KEYBOARD;
                    //input[2].ki.wVk = 0;
                    input[2].ki.wScan = this.ScanCode;
                    input[2].ki.dwFlags = (int)KEYEVENTF.SCANCODE | (int)KEYEVENTF.KEYUP;
                    //input[2].ki.time = 0;
                    input[2].ki.dwExtraInfo = IntPtr.Zero;

                    input[3].type = (int)InputType.INPUT_KEYBOARD;
                    //input[3].ki.wVk = 0;
                    input[3].ki.wScan = SHIFT;
                    input[3].ki.dwFlags = (int)KEYEVENTF.SCANCODE | (int)KEYEVENTF.KEYUP;
                    //input[3].ki.time = 0;
                    input[3].ki.dwExtraInfo = IntPtr.Zero;

                    SendInput((uint)input.Length, input, Marshal.SizeOf((object)default(INPUT)));
                }
                else
                {
                    INPUT[] input = new INPUT[2];

                    input[0].type = (int)InputType.INPUT_KEYBOARD;
                    //input[0].ki.wVk = 0;
                    input[0].ki.wScan = this.ScanCode;
                    input[0].ki.dwFlags = (int)KEYEVENTF.SCANCODE;
                    //input[0].ki.time = 0;
                    input[0].ki.dwExtraInfo = IntPtr.Zero;

                    input[1].type = (int)InputType.INPUT_KEYBOARD;
                    //input[1].ki.wVk = 0;
                    input[1].ki.wScan = this.ScanCode;
                    input[1].ki.dwFlags = (int)KEYEVENTF.SCANCODE | (int)KEYEVENTF.KEYUP;
                    //input[1].ki.time = 0;
                    input[1].ki.dwExtraInfo = IntPtr.Zero;

                    SendInput((uint)input.Length, input, Marshal.SizeOf((object)default(INPUT)));
                }
                System.Diagnostics.Debug.WriteLine(string.Format("push {0}", this.ScanCode));
            }
        }

        public Dictionary<string, Key> VirtualKeyDict = new Dictionary<string, Key>()
        {
            {"1", new Key("1",0x31,0x02,false)},
            {"2", new Key("2",0x32,0x03,false)},
            {"3", new Key("3",0x33,0x04,false)},
            {"4", new Key("4",0x34,0x05,false)},
            {"5", new Key("5",0x35,0x06,false)},
            {"6", new Key("6",0x36,0x07,false)},
            {"7", new Key("7",0x37,0x08,false)},
            {"8", new Key("8",0x38,0x09,false)},
            {"9", new Key("9",0x39,0x0a,false)},
            {"0", new Key("0",0x30,0x0b,false)},
            {"-", new Key("-",0x00,0xc,false)},
            {"=", new Key("=",0x00,0xd,false)},

            {"!", new Key("!",0x00,0x2,true)},
            {"@", new Key("@",0x00,0x3,true)},
            {"#", new Key("#",0x00,0x4,true)},
            {"$", new Key("$",0x00,0x5,true)},
            {"%", new Key("%",0x00,0x6,true)},
            {"^", new Key("^",0x00,0x7,true)},
            {"&", new Key("&",0x00,0x8,true)},
            {"*", new Key("*",0x00,0x9,true)},
            {"(", new Key("(",0x00,0xa,true)},
            {")", new Key(")",0x00,0xb,true)},
            {"_", new Key("_",0x00,0xc,true)},
            {"+", new Key("+",0x00,0xd,true)},

            {"q", new Key("q",0x71,0x10,false)},
            {"w", new Key("w",0x77,0x11,false)},
            {"e", new Key("e",0x65,0x12,false)},
            {"r", new Key("r",0x72,0x13,false)},
            {"t", new Key("t",0x74,0x14,false)},
            {"y", new Key("y",0x79,0x15,false)},
            {"u", new Key("u",0x75,0x16,false)},
            {"i", new Key("i",0x69,0x17,false)},
            {"o", new Key("o",0x6f,0x18,false)},
            {"p", new Key("p",0x70,0x19,false)},

            {"a", new Key("a",0x61,0x1e,false)},
            {"s", new Key("s",0x73,0x1f,false)},
            {"d", new Key("d",0x64,0x20,false)},
            {"f", new Key("f",0x66,0x21,false)},
            {"g", new Key("g",0x67,0x22,false)},
            {"h", new Key("h",0x68,0x23,false)},
            {"j", new Key("j",0x6a,0x24,false)},
            {"k", new Key("k",0x6b,0x25,false)},
            {"l", new Key("l",0x6c,0x26,false)},

            {"z", new Key("z",0x7a,0x2c,false)},
            {"x", new Key("x",0x78,0x2d,false)},
            {"c", new Key("c",0x63,0x2e,false)},
            {"v", new Key("v",0x76,0x2f,false)},
            {"b", new Key("b",0x62,0x30,false)},
            {"n", new Key("n",0x6e,0x31,false)},
            {"m", new Key("m",0x6d,0x32,false)},

            {"Q", new Key("Q",0x00,0x10,true)},
            {"W", new Key("W",0x00,0x11,true)},
            {"E", new Key("E",0x00,0x12,true)},
            {"R", new Key("R",0x00,0x13,true)},
            {"T", new Key("T",0x00,0x14,true)},
            {"Y", new Key("Y",0x00,0x15,true)},
            {"U", new Key("U",0x00,0x16,true)},
            {"I", new Key("I",0x00,0x17,true)},
            {"O", new Key("O",0x00,0x18,true)},
            {"P", new Key("P",0x00,0x19,true)},

            {"A", new Key("A",0x00,0x1e,true)},
            {"S", new Key("S",0x00,0x1f,true)},
            {"D", new Key("D",0x00,0x20,true)},
            {"F", new Key("F",0x00,0x21,true)},
            {"G", new Key("G",0x00,0x22,true)},
            {"H", new Key("H",0x00,0x23,true)},
            {"J", new Key("J",0x00,0x24,true)},
            {"K", new Key("K",0x00,0x25,true)},
            {"L", new Key("L",0x00,0x26,true)},

            {"Z", new Key("Z",0x00,0x2c,true)},
            {"X", new Key("X",0x00,0x2d,true)},
            {"C", new Key("C",0x00,0x2e,true)},
            {"V", new Key("V",0x00,0x2f,true)},
            {"B", new Key("B",0x00,0x30,true)},
            {"N", new Key("N",0x00,0x31,true)},
            {"M", new Key("M",0x00,0x32,true)},

            {"[", new Key("[",0x00,0x1a,false)},
            {"]", new Key("]",0x00,0x1b,false)},
            {";", new Key(";",0x00,0x27,false)},
            {"'", new Key("'",0x00,0x28,false)},
            {"`", new Key("`",0x00,0x29,false)},
            {"\\", new Key("\\",0x00,0x2b,false)},
            {",", new Key(",",0x00,0x33,false)},
            {".", new Key(".",0x00,0x34,false)},
            {"/", new Key("/",0x00,0x35,false)},

            {"{", new Key("{",0x00,0x1a,true)},
            {"}", new Key("}",0x00,0x1b,true)},
            {":", new Key(":",0x00,0x27,true)},
            {"\"", new Key("\"",0x00,0x28,true)},
            {"~", new Key("~",0x00,0x29,true)},
            {"|", new Key("|",0x00,0x2b,true)},
            {"<", new Key("<",0x00,0x33,true)},
            {">", new Key(">",0x00,0x34,true)},
            {"?", new Key("?",0x00,0x35,true)},

            {"F1"   , new Key("F1"   ,0x3b,0x00,false)},
            {"F2"   , new Key("F2"   ,0x3c,0x00,false)},
            {"F3"   , new Key("F3"   ,0x3d,0x00,false)},
            {"F4"   , new Key("F4"   ,0x3e,0x00,false)},
            {"F5"   , new Key("F5"   ,0x3f,0x00,false)},
            {"F6"   , new Key("F6"   ,0x40,0x00,false)},
            {"F7"   , new Key("F7"   ,0x41,0x00,false)},
            {"F8"   , new Key("F8"   ,0x42,0x00,false)},
            {"F9"   , new Key("F9"   ,0x43,0x00,false)},
            {"F10"  , new Key("F10"  ,0x44,0x00,false)},
            {"F11"  , new Key("F11"  ,0x85,0x00,false)},
            {"F12"  , new Key("F12"  ,0x86,0x00,false)},
            {"HOME" , new Key("HOME" ,0x47,0x00,false)},
            {"UP"   , new Key("UP"   ,0x48,0x00,false)},
            {"PGUP" , new Key("PGUP" ,0x49,0x00,false)},
            {"LEFT" , new Key("LEFT" ,0x4b,0x00,false)},
            {"RIGHT", new Key("RIGHT",0x4d,0x00,false)},
            {"END"  , new Key("END"  ,0x4f,0x00,false)},
            {"DOWN" , new Key("DOWN" ,0x50,0x00,false)},
            {"PGDN" , new Key("PGDN" ,0x51,0x00,false)},
            {"INS"  , new Key("INS"  ,0x52,0x00,false)},
            {"DEL"  , new Key("DEL"  ,0x53,0x00,false)}
        };
    }
}
