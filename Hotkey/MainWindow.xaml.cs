using System;
using System.Collections.Generic;
using System.Configuration;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Interop;
using System.Windows.Media;

namespace Hotkey
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    /// 
    public class FsModKey
    {
        public string Name { get; set; }
        public int Value { get; set; }
    }
    public class MyBase64
    {
        /// <summary>
        /// Base64加密，采用utf8编码方式加密
        /// </summary>
        /// <param name="source">待加密的明文</param>
        /// <returns>加密后的字符串</returns>
        public static string Base64Encode(string source)
        {
            return Base64Encode(Encoding.UTF8, source);
        }

        /// <summary>
        /// Base64加密
        /// </summary>
        /// <param name="encodeType">加密采用的编码方式</param>
        /// <param name="source">待加密的明文</param>
        /// <returns></returns>
        public static string Base64Encode(Encoding encodeType, string source)
        {
            string encode = string.Empty;
            byte[] bytes = encodeType.GetBytes(source);
            try
            {
                encode = Convert.ToBase64String(bytes);
            }
            catch
            {
                encode = source;
            }
            return encode;
        }

        /// <summary>
        /// Base64解密，采用utf8编码方式解密
        /// </summary>
        /// <param name="result">待解密的密文</param>
        /// <returns>解密后的字符串</returns>
        public static string Base64Decode(string result)
        {
            return Base64Decode(Encoding.UTF8, result);
        }

        /// <summary>
        /// Base64解密
        /// </summary>
        /// <param name="encodeType">解密采用的编码方式，注意和加密时采用的方式一致</param>
        /// <param name="result">待解密的密文</param>
        /// <returns>解密后的字符串</returns>
        public static string Base64Decode(Encoding encodeType, string result)
        {
            string decode = string.Empty;
            byte[] bytes = Convert.FromBase64String(result);
            try
            {
                decode = encodeType.GetString(bytes);
            }
            catch
            {
                decode = result;
            }
            return decode;
        }
    }
    public partial class MainWindow : Window
    {
        [DllImport("user32.dll", EntryPoint = "RegisterHotKey")]
        public static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vk);
        [DllImport("user32.dll", EntryPoint = "UnregisterHotKey")]
        public static extern bool UnregisterHotKey(IntPtr hWnd, int id);
        public struct HotKeyHanld
        {
            IntPtr hWnd;
            int id;
            int fsModifiers;
            int vk;
            List<VirtualKey.Key> action;
            public HotKeyHanld(IntPtr _hWnd, int _id, int _fsModifiers, int _vk, List<VirtualKey.Key> _action)
            {
                this.hWnd = _hWnd;
                this.id = _id;
                this.fsModifiers = _fsModifiers;
                this.vk = _vk;
                this.action = _action;
            }
            public void ARegisterHotKey()
            {
                // 注册热键 并添加至 HotKeyQueue 字典
                if (!RegisterHotKey(this.hWnd, this.id, this.fsModifiers, this.vk))
                {
                    // 热键注册失败
                    MessageBox.Show("RegisterHotKey fail", "err");
                    System.Diagnostics.Debug.WriteLine("RegisterHotKey fail");
                    return;
                }
                if (HotKeyQueue.ContainsKey(this.id))
                {
                    // key已存在
                    HotKeyQueue[this.id] = this;
                }
                else
                {
                    // 新建key
                    HotKeyQueue.Add(this.id, this);
                }
                System.Diagnostics.Debug.WriteLine("RegisterHotKey success");
            }
            public void AUnregisterHotKey()
            {
                // 卸载热键 并从 HotKeyQueue 字典中删除
                UnregisterHotKey(this.hWnd, this.id);
                System.Diagnostics.Debug.WriteLine("UnregisterHotKey success");
            }
            public void SendMsg()
            {
                // 队列顺序调用 VirtualKey 执行动作
                System.Diagnostics.Debug.WriteLine("SendMsg success");
                foreach (VirtualKey.Key elem in this.action)
                {
                    System.Diagnostics.Debug.WriteLine(string.Format("print {0}", elem.Character));
                    elem.PushKey();
                }
            }
        }
        public static IntPtr hd;
        static readonly VirtualKey VirtualKeys = new VirtualKey();
        private static Dictionary<int, HotKeyHanld> HotKeyQueue = new Dictionary<int, HotKeyHanld>();
        public static DefSettings defSettings = new DefSettings();
        public static List<StackPanel> Sps = new List<StackPanel> { };
        public MainWindow()
        {
            InitializeComponent();
        }
        public int GetComboValue(DependencyObject obj, out string vk, out string pass)
        {
            ComboBox combobox = VisualTreeHelper.GetChild(obj, 0) as ComboBox;
            TextBox textbox = VisualTreeHelper.GetChild(obj, 2) as TextBox;
            PasswordBox passwordbox = VisualTreeHelper.GetChild(obj, 3) as PasswordBox;

            int fsk;
            if (combobox.SelectedValue != null && textbox.Text != "" && passwordbox.Password != "")
            {
                // 组合键不为空 输出字符不为空
                System.Diagnostics.Debug.WriteLine(combobox.SelectedValue);
                System.Diagnostics.Debug.WriteLine(textbox.Text);
                System.Diagnostics.Debug.WriteLine(passwordbox.Password);

                vk = textbox.Text;
                pass = passwordbox.Password;
                fsk = (int)combobox.SelectedValue;
                return fsk;
            }
            else
            {
                System.Diagnostics.Debug.WriteLine("GetHkComb fail");
                vk = textbox.Text;
                pass = passwordbox.Password;
                return 0;
            }
        }
        private void Button_Register(object sender, RoutedEventArgs e)
        {
            foreach (KeyValuePair<int, HotKeyHanld> kv in HotKeyQueue)
            {
                Log(String.Format("UnregisterHotKey {0}", kv.Key));
                kv.Value.AUnregisterHotKey();
            }
            HotKeyQueue.Clear();// 清空 HotKeyQueue 字典

            int id = 10000;
            foreach (StackPanel stackPanel in Sps)
            {
                int fsk;
                fsk = GetComboValue(stackPanel, out string vk, out string pass);
                if (fsk > 0)
                {
                    int vki = VirtualKeys.VirtualKeyDict[vk].AsciiCode;
                    HotKeyQueue.Add(id, new HotKeyHanld(hd, id, fsk, vki, Getaction(pass)));
                    id += 1;

                    defSettings[stackPanel.Name] = fsk.ToString() + vk + MyBase64.Base64Encode(pass); //保存配置
                    defSettings.Save();
                }
            }

            List<int> keys = new List<int>(HotKeyQueue.Keys);
            for (int i = 0; i < keys.Count; i++)
            {
                Log(String.Format("RegisterHotKey {0}", keys[i]));
                HotKeyQueue[keys[i]].ARegisterHotKey();
            }
        }
        private void Log(string msg)
        {
            string input = String.Format("[{0}]  {1}", DateTime.Now.ToLongTimeString().ToString(), msg);
            Console.AppendText(input + Environment.NewLine);
        }
        protected override void OnSourceInitialized(EventArgs e)
        {
            base.OnSourceInitialized(e);
            hd = new WindowInteropHelper(this).Handle;
            HwndSource source = HwndSource.FromHwnd(hd);
            source.AddHook(WndProc);
        }
        protected override void OnClosed(EventArgs e)
        {
            foreach (KeyValuePair<int, HotKeyHanld> kv in HotKeyQueue)
            {
                kv.Value.AUnregisterHotKey();
            }
            base.OnClosed(e);
        }
        private void Window_Loaded(object sender, EventArgs e)
        {
            Sps.Add(hkA);
            Sps.Add(hkB);
            Sps.Add(hkC);
            Sps.Add(hkD);

            List<FsModKey> fsmodkey = new List<FsModKey> { };
            fsmodkey.Add(new FsModKey { Name = "Alt", Value = 0x0001 });
            fsmodkey.Add(new FsModKey { Name = "CtrL", Value = 0x0002 });
            fsmodkey.Add(new FsModKey { Name = "Shift", Value = 0x0004 });
            fsmodkey.Add(new FsModKey { Name = "Win", Value = 0x0008 });

            foreach (StackPanel stackPanel in Sps) //绑定下拉框
            {
                ComboBox combobox = VisualTreeHelper.GetChild(stackPanel, 0) as ComboBox;
                combobox.ItemsSource = fsmodkey;
                combobox.SelectedIndex = 0;
            }
            
            foreach (StackPanel stackPanel in Sps) //如果有 则加载配置
            {
                string value = defSettings[stackPanel.Name].ToString();

                if (value.Length < 3)
                {
                    continue;
                }

                ComboBox combobox = VisualTreeHelper.GetChild(stackPanel, 0) as ComboBox;
                TextBox textbox = VisualTreeHelper.GetChild(stackPanel, 2) as TextBox;
                PasswordBox passwordbox = VisualTreeHelper.GetChild(stackPanel, 3) as PasswordBox;
            
                switch(value.Substring(0, 1))
                {
                    case "2":
                        combobox.SelectedIndex = 1;
                        break;
                    case "1":
                        combobox.SelectedIndex = 0;
                        break;
                    case "4":
                        combobox.SelectedIndex = 2;
                        break;
                    case "8":
                        combobox.SelectedIndex = 3;
                        break;
                    default:
                        combobox.SelectedIndex = 0;
                        break;
                }
                textbox.Text = value.Substring(1, 1);
                passwordbox.Password = MyBase64.Base64Decode(value.Substring(2));
            }
        }
        private IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
        {
            // 监听系统消息 判断热键
            const int WM_HOTKEY = 0x0312;
            if (msg == WM_HOTKEY)
            {
                handled = true;
                //Mhotkey(wParam.ToInt32());
                if (HotKeyQueue.ContainsKey(wParam.ToInt32()))
                {
                    //
                    Thread.Sleep(1000);
                    HotKeyQueue[wParam.ToInt32()].SendMsg();
                }
            }
            return IntPtr.Zero;
        }
        public List<VirtualKey.Key> Getaction(string text)
        {
            char[] chars = text.ToCharArray();
            List<VirtualKey.Key> keys = new List<VirtualKey.Key>();
            foreach (char c in chars)
            {
                if (VirtualKeys.VirtualKeyDict.ContainsKey(c.ToString()))
                {
                    keys.Add(VirtualKeys.VirtualKeyDict[c.ToString()]);
                }
            }
            return keys;
        }
    }
    public sealed class DefSettings : ApplicationSettingsBase
    {
        [UserScopedSetting]
        [DefaultSettingValue("1")]
        public string hkA
        {
            get { return (string)this["hkA"]; }
            set { this["hkA"] = value; }
        }
        [UserScopedSetting]
        [DefaultSettingValue("4")]
        public string hkB
        {
            get { return (string)this["hkB"]; }
            set { this["hkB"] = value; }
        }
        [UserScopedSetting]
        [DefaultSettingValue("2")]
        public string hkC
        {
            get { return (string)this["hkC"]; }
            set { this["hkC"] = value; }
        }
        [UserScopedSetting]
        [DefaultSettingValue("8")]
        public string hkD
        {
            get { return (string)this["hkD"]; }
            set { this["hkD"] = value; }
        }
    }
}
