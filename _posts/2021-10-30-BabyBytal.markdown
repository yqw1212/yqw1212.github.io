---
layout: post
title:  Baby Bytal
date:   2021-10-30 08:00:01 +0300
image:  2021-10-30-cat.jpg
tags:   [ctf,reverse,metal,ios,ipa,Bytectf,shader]
---

解压.ipa文件，文件目录

```assembly
D:.
│  Assets.car
│  Bytal
│  default.metallib
│  Info.plist
│  PkgInfo
│
└─Base.lproj
   ├─LaunchScreen.storyboardc
   │      01J-lp-oVM-view-Ze5-6b-2t3.nib
   │      Info.plist
   │      UIViewController-01J-lp-oVM.nib
   │
   └─Main.storyboardc
           BYZ-38-t0r-view-8bC-Xf-vdC.nib
           Info.plist
           UIViewController-BYZ-38-t0r.nib
```

Bytal是一个二进制文件，default.metallib是Metal 二进制动态库文件。

在本题中`.metallib` 文件没有以 release 模式编译，而是以 debug 模式编译。在 debug 模式中，为了便于图形相关功能的开发与调试，shader源代码会附带到 Metal 二进制动态库中，但这也为第三方获取源代码提供了可能性。

> binwalk default.metallib -e

得到三个文件

```assembly
D:.
    30B7
    40C9
    50DB
```

其中40C9即shader源代码

```assembly
#include <metal_stdlib>

using namespace metal;

kernel void l3337(texture2d<float, access::read> inTexture [[texture(0)]],
                  texture2d<float, access::write> outTexture [[texture(1)]],
                  constant float &time [[buffer(0)]],
                  uint2 gid [[thread_position_in_grid]])
{
    
    uint2 textureIndex(gid.x, gid.y);
    float4 color = inTexture.read(textureIndex).rgba;
    
    float f1a9 = 0.25966575119248700544433461867386159912576603454284701873271675165943630180804960680077068794525951833662702483707107603549957275390625;
    float f1ag = 0.2242033719552458840313293105033220925053855333108149760985058882708434515078364431563838469097134364904633230253239162266254425048828125;
    float fla9 = 0.2077849030914869249521744496157905766607367128092953819257027517188506521123914610222981787777431217367762883441173471510410308837890625;
    
    outTexture.write(float4(color.rgb * max(f1a9 * sin(time / fla9 + f1ag) + fla9, 0.0), 1), gid);
}
```

将三个小数转为十六进制并拼接

```assembly
from math import floor
from fractions import Fraction

def convert(x):
    ans = []
    while x > 0:
        x = x * 256
        floor_x = floor(x)
        x = x - floor_x
        ans.append(chr(floor_x))
    return ''.join(ans)

flags = [
    '0.25966575119248700544433461867386159912576603454284701873271675165943630180804960680077068794525951833662702483707107603549957275390625',
    '0.2242033719552458840313293105033220925053855333108149760985058882708434515078364431563838469097134364904633230253239162266254425048828125',
    '0.2077849030914869249521744496157905766607367128092953819257027517188506521123914610222981787777431217367762883441173471510410308837890625',
]

for i in flags:
    print(convert(Fraction(i)))
```

ByteCTF{036d3afcd51d3af23c2f099b2a9edf3aa9edd49bd4}
