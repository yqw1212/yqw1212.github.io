---
layout: post
title:  StudyDesk
date:   2021-10-23 00:08:01 +0300
image:  2021-10-23-monastery.jpg
tags:   [ctf,reverse,mobile,android,强网拟态防御]
---

MainActivity

```assembly
package com.test.studydesk;

import android.text.method.KeyListener;
import android.util.Log;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Toast;
import b.c.a.a;
import java.io.ByteArrayOutputStream;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

public class MainActivity$a implements View$OnClickListener {
    public MainActivity$a(MainActivity arg1) {
        this.b = arg1;
        super();
    }

    public void onClick(View arg15) {
        String v11;
        BigDecimal v10;
        int v4_1;
        int v9;
        KeyListener v7;
        String v15 = this.b.o.getText().toString();
        int v2 = 0x20;
        if(v15.length() != v2) {
        }
        else {
            byte[] v0 = a.a;
            ByteArrayOutputStream v3 = new ByteArrayOutputStream();
            StringBuilder v4 = new StringBuilder();
            int v5 = v0.length;
            int v6 = 0;
            while(true) {
                v7 = null;
                if(v6 < v5) {
                    v9 = v15.indexOf(v0[v6]);
                    if(v9 == -1) {
                        v0 = ((byte[])v7);
                    }
                    else {
                        v4.append(Integer.toBinaryString((v9 & 0x3F) + v2).substring(1));
                        ++v6;
                        continue;
                    }
                }
                else {
                    break;
                }

                goto label_56;
            }

            int v0_1;
            for(v0_1 = 0; v0_1 < (40 - v4.length() % 40) % 40; ++v0_1) {
                v4.append('0');
            }

            String v0_2 = v4.toString();
            for(v2 = 0; v2 < v0_2.length(); v2 = v4_1) {
                v4_1 = v2 + 8;
                v3.write(((byte)(Integer.parseInt(v0_2.substring(v2, v4_1), 2) & 0xFF)));
            }

            v0 = v3.toByteArray();
        label_56:
            if(v0 == null) {
                goto label_157;
            }

            BigDecimal v2_1 = new BigDecimal("1");
            BigDecimal v3_1 = new BigDecimal("0");
            BigDecimal v4_2 = new BigDecimal("6");
            MathContext v5_1 = new MathContext(360, RoundingMode.HALF_UP);
            MathContext v6_1 = new MathContext(720, RoundingMode.HALF_UP);
            v9 = 0;
            while(true) {
                v2_1 = a.a(new BigDecimal("2").subtract(a.a(new BigDecimal(4).subtract(v2_1.multiply(v2_1, v6_1), v6_1), v6_1)), v6_1);
                v4_2 = new BigDecimal("2").multiply(v4_2, v5_1);
                v10 = new BigDecimal("0.5").multiply(v2_1.multiply(v4_2, v5_1), v5_1);
                v11 = "StudyDesk:";
                if(v10.compareTo(v3_1) == 0) {
                    break;
                }

                ++v9;
                if(v9 % 30 == 0) {
                    StringBuilder v3_2 = b.a.a.a.a.e("running: ");
                    v3_2.append(v9 / 6);
                    v3_2.append("%");
                    Log.i(v11, v3_2.toString());
                }

                v3_1 = v10;
            }

            Log.i(v11, "running: 100%");
            String v2_2 = v10.toString().replace(".", "");
            int v3_3 = 0;
            while(true) {
                if(v3_3 < v2_2.length()) {
                    v4_1 = v3_3 + 2;
                    if((((byte)(Integer.parseInt(v2_2.substring(v3_3, v4_1), 10) & 0xFF))) != v0[v3_3 / 2]) {
                        v0_1 = 0;
                    }
                    else {
                        v3_3 = v4_1;
                        continue;
                    }
                }
                else {
                    break;
                }

                goto label_120;
            }

            v0_1 = 1;
        label_120:
            if(v0_1 == 0) {
                goto label_157;
            }

            Toast.makeText(this.b, "Congs, good student!", 0).show();
            this.b.q.setText(String.format("flag{"+v15+"}"));
            this.b.p.setText("Congs!");
            this.b.p.setClickable(false);
            this.b.o.setKeyListener(v7);
            return;
        }

    label_157:
        Toast.makeText(this.b, "Nonono, study harder please", 0).show();
    }
}
```

a类

```assembly
package b.c.a;

import java.math.BigDecimal;
import java.math.MathContext;

public class a {
    public static byte[] a;

    public static {
        a.a = new byte[]{0x73, 0x6F, 43, 0x72, 0x74, 45, 0x30, 36, 84, 98, 89, 36, 38, 66, 38, 43, 84, 0x79, 50, 101, 101, 43, 100, 87, 69, 0x6F, 51, 66, 89, 49, 69, 51, 101, 51, 53, 0x74, 45, 98, 98, 0x72, 50, 36, 98, 50, 85, 85, 85, 107, 66, 36, 53, 51, 0x6F, 0x72, 89, 89, 66, 50, 33, 66, 0x5F, 66, 101, 0x79, 0x5F, 0x40, 33, 66, 50, 0x40, 85, 85, 45, 43, 36, 50, 0x74, 0x30, 85, 0x73, 0x5F, 0x40, 49, 0x72, 50, 101, 101, 51, 51, 43, 53, 51, 53, 51, 85, 50, 0x40, 0x79, 53, 36, 0x40, 69, 89, 98, 45, 0x6F, 101, 36, 97, 66, 100, 0x30, 0x73, 97, 0x30, 36, 0x6F, 101, 50, 0x5F, 49, 0x30, 0x40, 89, 0x74, 85, 0x30, 85, 0x73, 89, 43, 89, 97, 0x30, 89, 0x72, 97, 100, 38, 50, 0x74, 51, 98, 0x75, 0x5F, 50, 0x74, 0x73, 0x6F, 84, 98, 89, 69, 0x6F, 100, 0x30, 0x6F, 98, 89, 0x72, 0x40, 50, 36, 66, 89, 101, 0x72, 51, 84, 51, 50, 36, 38, 0x40, 0x30, 53, 51, 0x30, 49, 97, 0x74, 89, 101, 85, 97, 66, 84, 97, 45, 43, 100, 89, 45, 0x30, 0x73, 0x30, 0x40, 97, 100, 98, 51, 100, 0x6F, 0x73, 50, 53, 101, 66, 101, 0x6F, 0x75, 50, 45, 0x5F, 51, 82, 50, 89, 87, 101, 50, 89, 0x30, 89, 101, 43, 89, 36, 38, 61, 101, 0x40, 84, 89, 0x5F, 66, 0x74, 49, 0x40, 87, 97, 43, 0x5F, 0x73, 43, 0x30, 89, 45, 84, 89, 33, 89, 107, 53, 85, 0x30, 98, 98, 0x5F, 50, 107, 66, 101, 0x6F, 51, 97, 33, 66, 97, 0x75, 51, 0x74, 51, 97, 0x40, 89, 107, 98, 51, 69, 0x40, 73, 0x5F, 0x30, 85, 0x74, 0x30, 97};
    }

    public static BigDecimal a(BigDecimal arg3, MathContext arg4) {
        BigDecimal v1;
        BigDecimal v0;
        for(v0 = arg3; true; v0 = v1) {
            v1 = new BigDecimal("0.5").multiply(v0.add(arg3.divide(v0, arg4), arg4), arg4);
            if(v1.compareTo(v0) == 0) {
                return v1;
            }
        }

        return v1;
    }
}
```

优化代码

```assembly
package job;

import java.awt.event.KeyListener;
import java.io.ByteArrayOutputStream;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

/**
 * @author: yqw
 * @date: 2021/10/23
 * @description:
 */
public class StudyDesk {
    public static void main(String[] args) {

        int v4_1;

        String v15 = "flag{abcdefghijklmnopqrstuvwxyz}";
        if (v15.length() == 0x20) {
            byte[] v0 = new byte[]{0x73, 0x6F, 43, 0x72, 0x74, 45, 0x30, 36, 84, 98, 89, 36, 38, 66, 38, 43, 84, 0x79, 50, 101, 101, 43, 100, 87, 69, 0x6F, 51, 66, 89, 49, 69, 51, 101, 51, 53, 0x74, 45, 98, 98, 0x72, 50, 36, 98, 50, 85, 85, 85, 107, 66, 36, 53, 51, 0x6F, 0x72, 89, 89, 66, 50, 33, 66, 0x5F, 66, 101, 0x79, 0x5F, 0x40, 33, 66, 50, 0x40, 85, 85, 45, 43, 36, 50, 0x74, 0x30, 85, 0x73, 0x5F, 0x40, 49, 0x72, 50, 101, 101, 51, 51, 43, 53, 51, 53, 51, 85, 50, 0x40, 0x79, 53, 36, 0x40, 69, 89, 98, 45, 0x6F, 101, 36, 97, 66, 100, 0x30, 0x73, 97, 0x30, 36, 0x6F, 101, 50, 0x5F, 49, 0x30, 0x40, 89, 0x74, 85, 0x30, 85, 0x73, 89, 43, 89, 97, 0x30, 89, 0x72, 97, 100, 38, 50, 0x74, 51, 98, 0x75, 0x5F, 50, 0x74, 0x73, 0x6F, 84, 98, 89, 69, 0x6F, 100, 0x30, 0x6F, 98, 89, 0x72, 0x40, 50, 36, 66, 89, 101, 0x72, 51, 84, 51, 50, 36, 38, 0x40, 0x30, 53, 51, 0x30, 49, 97, 0x74, 89, 101, 85, 97, 66, 84, 97, 45, 43, 100, 89, 45, 0x30, 0x73, 0x30, 0x40, 97, 100, 98, 51, 100, 0x6F, 0x73, 50, 53, 101, 66, 101, 0x6F, 0x75, 50, 45, 0x5F, 51, 82, 50, 89, 87, 101, 50, 89, 0x30, 89, 101, 43, 89, 36, 38, 61, 101, 0x40, 84, 89, 0x5F, 66, 0x74, 49, 0x40, 87, 97, 43, 0x5F, 0x73, 43, 0x30, 89, 45, 84, 89, 33, 89, 107, 53, 85, 0x30, 98, 98, 0x5F, 50, 107, 66, 101, 0x6F, 51, 97, 33, 66, 97, 0x75, 51, 0x74, 51, 97, 0x40, 89, 107, 98, 51, 69, 0x40, 73, 0x5F, 0x30, 85, 0x74, 0x30, 97};
            ByteArrayOutputStream v3 = new ByteArrayOutputStream();
            StringBuilder v4 = new StringBuilder();

            int v6 = 0;
            while (v6 < v0.length) {

                int v9 = v15.indexOf(v0[v6]);
                if (v9 != -1) {
                    v4.append(Integer.toBinaryString((v9 & 0x3F) + 0x20).substring(1));
                    ++v6;
                }
                // G
            }

            v4.append("0".repeat((40 - v4.length() % 40) % 40));

            String v0_2 = v4.toString();
            for (int v2 = 0; v2 < v0_2.length(); v2 = v4_1) {
                v4_1 = v2 + 8;
                v3.write(((byte) (Integer.parseInt(v0_2.substring(v2, v4_1), 2) & 0xFF)));
            }

            v0 = v3.toByteArray();
            BigDecimal v2_1 = new BigDecimal("1");
            BigDecimal v3_1 = new BigDecimal("0");
            BigDecimal v4_2 = new BigDecimal("6");
            MathContext v5_1 = new MathContext(360, RoundingMode.HALF_UP);
            MathContext v6_1 = new MathContext(720, RoundingMode.HALF_UP);

            BigDecimal v10;
            while (true) {
                v2_1 = a(new BigDecimal("2").subtract(a(new BigDecimal(4).subtract(v2_1.multiply(v2_1, v6_1), v6_1), v6_1)), v6_1);
                v4_2 = new BigDecimal("2").multiply(v4_2, v5_1);
                v10 = new BigDecimal("0.5").multiply(v2_1.multiply(v4_2, v5_1), v5_1);
                if (v10.compareTo(v3_1) == 0) {
                    break;
                }

                v3_1 = v10;
            }
            // running: 100%
            String v2_2 = v10.toString().replace(".", "");
            int v3_3 = 0;
            while (v3_3 < v2_2.length()) {

                v4_1 = v3_3 + 2;
                if ((((byte) (Integer.parseInt(v2_2.substring(v3_3, v4_1), 10) & 0xFF))) == v0[v3_3 / 2]) {
                    v3_3 = v4_1;
                }

                // G
            }

            System.out.println("flag{" + v15 + "}");
        }
    }

    public static BigDecimal a(BigDecimal arg3, MathContext arg4) {
        BigDecimal v1;
        BigDecimal v0;
        for(v0 = arg3; true; v0 = v1) {
            v1 = new BigDecimal("0.5").multiply(v0.add(arg3.divide(v0, arg4), arg4), arg4);
            if(v1.compareTo(v0) == 0) {
                return v1;
            }
        }
    }
}
```

索引：[0, 0x20)

索引：[0, 00100000)

&0x3F: [0, 00100000)

+0x20: [00100000, 01000000)

```assembly
package job;

import java.awt.event.KeyListener;
import java.io.ByteArrayOutputStream;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.Arrays;

/**
 * @author: yqw
 * @date: 2021/10/23
 * @description:
 */
public class StudyDesk {
    public static void main(String[] args) {

//        BigDecimal v2_1 = new BigDecimal("1");
//        BigDecimal v3_1 = new BigDecimal("0");
//        BigDecimal v4_2 = new BigDecimal("6");
//        MathContext v5_1 = new MathContext(360, RoundingMode.HALF_UP);
//        MathContext v6_1 = new MathContext(720, RoundingMode.HALF_UP);
//
//        BigDecimal v10;
//        while (true) {
//            v2_1 = a(new BigDecimal("2").subtract(a(new BigDecimal(4).subtract(v2_1.multiply(v2_1, v6_1), v6_1), v6_1)), v6_1);
//            v4_2 = new BigDecimal("2").multiply(v4_2, v5_1);
//            v10 = new BigDecimal("0.5").multiply(v2_1.multiply(v4_2, v5_1), v5_1);
//            if (v10.compareTo(v3_1) == 0) {
//                break;
//            }
//
//            v3_1 = v10;
//        }
          String v2_2 = v10.toString().replace(".", "");
//        System.out.println(v2_2);
        // 314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036

        System.out.println(v2_2.length());
        int v3_3 = 0;

        byte[] v0 = new byte[180];

        while (v3_3 < v2_2.length()) {
//            System.out.println((byte) (Integer.parseInt(v2_2.substring(v3_3, v3_3+2), 10) & 0xFF));
            v0[v3_3/2] = (byte) Integer.parseInt(v2_2.substring(v3_3, v3_3+2));
            v3_3 += 2;
        }

        System.out.println(Arrays.toString(v0));

        //test
//        ByteArrayOutputStream v3 = new ByteArrayOutputStream();
//        v3.write(((byte) (Integer.parseInt("00001000", 2) & 0xFF)));
//        byte aa[] = v3.toByteArray();
//        System.out.println(Arrays.toString(aa));

        //此处用python脚本拼接得到

        String v4 = "000111110010100100111011000110100011010100111010011000010101110100010111010101000011111001000000001000010101001100011011010111110000001001011000001010010110000100010000010111010110001100100101001100110000010101010010000010010100101001011110001011010101110000011110010011100001000000101000001111100101011000010100010110010110001000111110010100000010001001010010001101010010101000001011010001100100001101100010000101010011000000001000010000010000110100011100000101110000011001000000010001100101110101010100001011100000100100110111000001010101001000010111000100010001100100100011010111100000100000001100010101000101000100001011010010100011001000011100001010010000001001000110000100110010011000110100000010110000010100110111011000000010110000111110000111010011000001011111001100010001111000100110000100110100000000101010010110000000101001100001001110000100000101011101001000100010111000001100010101000100101101000000010100100010000101001110010000110101001100010000001101000100011100010100000100110000100100001110001110000011000000111000010001010001011100101110000000110011000000111101000001000011011000100000010000100011000000010101001000010101110100111100010010000011110000011000010110110010100100011011001001010001100000111010010001100000011000111100001111110000111100111010010100010100101001011000000011110001010001011100000010010011111001010010010111000011011000001001000100010000111100100100001010110100001101011001000110010101101000100100";
        // 1440


        // test
        String subStr = Integer.toBinaryString((0x43 & 0x3F) + 0x20);
        System.out.println(subStr);
        System.out.println(Integer.toBinaryString((0x43 & 0x3F) + 0x20).substring(1));


        int[] index = new int[288];
        int point = 0;
        for(int i=0; i<1440; i+=5){
            String num = "1" + v4.substring(i, i+5);
            index[point++] = Integer.parseInt(num, 2)-0x20;
        }
        System.out.println(Arrays.toString(index));

        byte[] flag = new byte[32];
        byte[] data = new byte[]{0x73, 0x6F, 43, 0x72, 0x74, 45, 0x30, 36, 84, 98, 89, 36, 38, 66, 38, 43, 84, 0x79, 50, 101, 101, 43, 100, 87, 69, 0x6F, 51, 66, 89, 49, 69, 51, 101, 51, 53, 0x74, 45, 98, 98, 0x72, 50, 36, 98, 50, 85, 85, 85, 107, 66, 36, 53, 51, 0x6F, 0x72, 89, 89, 66, 50, 33, 66, 0x5F, 66, 101, 0x79, 0x5F, 0x40, 33, 66, 50, 0x40, 85, 85, 45, 43, 36, 50, 0x74, 0x30, 85, 0x73, 0x5F, 0x40, 49, 0x72, 50, 101, 101, 51, 51, 43, 53, 51, 53, 51, 85, 50, 0x40, 0x79, 53, 36, 0x40, 69, 89, 98, 45, 0x6F, 101, 36, 97, 66, 100, 0x30, 0x73, 97, 0x30, 36, 0x6F, 101, 50, 0x5F, 49, 0x30, 0x40, 89, 0x74, 85, 0x30, 85, 0x73, 89, 43, 89, 97, 0x30, 89, 0x72, 97, 100, 38, 50, 0x74, 51, 98, 0x75, 0x5F, 50, 0x74, 0x73, 0x6F, 84, 98, 89, 69, 0x6F, 100, 0x30, 0x6F, 98, 89, 0x72, 0x40, 50, 36, 66, 89, 101, 0x72, 51, 84, 51, 50, 36, 38, 0x40, 0x30, 53, 51, 0x30, 49, 97, 0x74, 89, 101, 85, 97, 66, 84, 97, 45, 43, 100, 89, 45, 0x30, 0x73, 0x30, 0x40, 97, 100, 98, 51, 100, 0x6F, 0x73, 50, 53, 101, 66, 101, 0x6F, 0x75, 50, 45, 0x5F, 51, 82, 50, 89, 87, 101, 50, 89, 0x30, 89, 101, 43, 89, 36, 38, 61, 101, 0x40, 84, 89, 0x5F, 66, 0x74, 49, 0x40, 87, 97, 43, 0x5F, 0x73, 43, 0x30, 89, 45, 84, 89, 33, 89, 107, 53, 85, 0x30, 98, 98, 0x5F, 50, 107, 66, 101, 0x6F, 51, 97, 33, 66, 97, 0x75, 51, 0x74, 51, 97, 0x40, 89, 107, 98, 51, 69, 0x40, 73, 0x5F, 0x30, 85, 0x74, 0x30, 97};
//        System.out.println(data.length);
        // 288
        for(int i=0; i<288; i++){
            flag[index[i]] = data[i];
        }


        System.out.println("flag{" + new String(flag) + "}");

    }

    public static BigDecimal a(BigDecimal arg3, MathContext arg4) {
        BigDecimal v1;
        BigDecimal v0;
        for(v0 = arg3; true; v0 = v1) {
            v1 = new BigDecimal("0.5").multiply(v0.add(arg3.divide(v0, arg4), arg4), arg4);
            if(v1.compareTo(v0) == 0) {
                return v1;
            }
        }
    }
}
```

具体过程不想分析了，太累了

flag{23esaB-T@b1E_I5=Y0Ur+$tudy&WoRk!}