using System;

namespace job
{
    class Program
    {
        static void Main(string[] args)
        {
            string s = decoder4("\v\fP\u000e\u000fBA\u0006\rG\u0015I\u001a\u0001\u0016H\\\t\b\u0002\u0013/\b\t^\u001d\bJO\a]C\u001b\u0005");
            Console.WriteLine(s);
        }

        static public string decoder2(string encoded)
        {
        string str1 = "";
        string str2 = "this";
        for (int index = 0; index < encoded.Length; ++index)
            str1 = str1 + (object) (char) ((uint) encoded[index] ^ (uint) str2[index % str2.Length]);
        return str1;
        }

        static public string decoder4(string encoded)
        {
        string str1 = "";
        string str2 = decoder2("\x001B\x0005\x000ES\x001D\x001BI\a\x001C\x0001\x001AS\0\0\fS\x0006\r\b\x001FT\a\a\x0016K");
        for (int index = 0; index < encoded.Length; ++index)
            str1 = str1 + (object) (char) ((uint) encoded[index] ^ (uint) str2[index % str2.Length]);
        return str1;
        }

        // static public string decoder4(string encoded)
		// {
		// 	string text = "";
		// 	string text2 = decoder2("\u001b\u0005\u000eS\u001d\u001bI\a\u001c\u0001\u001aS\0\0\fS\u0006\r\b\u001fT\a\a\u0016K");
		// 	for (int i = 0; i < encoded.Length; i++)
		// 	{
		// 		text += (encoded[i] ^ text2[i % text2.Length]);
		// 	}
		// 	return text;
		// }

        // static public string decoder2(string encoded)
		// {
		// 	string text = "";
		// 	string text2 = "this";
		// 	for (int i = 0; i < encoded.Length; i++)
		// 	{
		// 		text += (encoded[i] ^ text2[i % text2.Length]);
		// 	}
		// 	return text;
		// }
    }
}
