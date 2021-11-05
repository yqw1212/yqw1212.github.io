---
layout: post
title:  Mother Bytal
date:   2021-10-31 08:00:01 +0300
image:  2021-10-31-italy.jpg
tags:   [ctf,reverse,metal,ios,ipa,Bytectf,shader]
---

解压ipa得到.metallib文件，由于`.metallib` 文件没有以 release 模式编译，而是以 debug 模式编译。在 debug 模式中，为了便于图形相关功能的开发调试，shader源代码会附带到 Metal 二进制动态库中

binwalk提取得到shader源代码

```assembly
#include <metal_stdlib>

using namespace metal;

kernel void l3337(texture2d<float, access::read> inTexture [[texture(0)]],
                  texture2d<float, access::write> outTexture [[texture(1)]],
                  constant float &time [[buffer(0)]],
                  uint2 gid [[thread_position_in_grid]])
{
    int w = inTexture.get_width();
    int h = inTexture.get_height();
    
    if(!(w == 9 && h == 9))
    {
        outTexture.write(float4(0, 0, 0, 0), gid);
        return;
    }
    
    int x0 = (gid.x + w - 2) % w;
    int x1 = (gid.x + w - 1) % w;
    int x2 = gid.x;
    int x3 = (gid.x + 1) % w;
    int x4 = (gid.x + 2) % w;
    
    int y0 = (gid.y + h - 2) % h;
    int y1 = (gid.y + h - 1) % h;
    int y2 = gid.y;
    int y3 = (gid.y + 1) % h;
    int y4 = (gid.y + 2) % h;
    
    float3 color = float3(0, 0, 0);
    color += inTexture.read(uint2(x4, y4)).xxy;
    color += inTexture.read(uint2(x2, y1)).zzz;
    color += inTexture.read(uint2(x4, y1)).zzx;
    color += inTexture.read(uint2(x1, y3)).zyx;
    color += inTexture.read(uint2(x3, y2)).zyy;
    color += inTexture.read(uint2(x0, y4)).yyx;
    color += inTexture.read(uint2(x4, y0)).xzz;
    color += inTexture.read(uint2(x4, y0)).zxy;
    color += inTexture.read(uint2(x4, y2)).xxz;
    color += inTexture.read(uint2(x3, y4)).xyx;
    color += inTexture.read(uint2(x0, y4)).zzx;
    color += inTexture.read(uint2(x3, y4)).yxx;
    color += inTexture.read(uint2(x4, y4)).zzx;
    color += inTexture.read(uint2(x2, y1)).yyz;
    color += inTexture.read(uint2(x3, y0)).yyy;
    color += inTexture.read(uint2(x1, y3)).yxz;
    color += inTexture.read(uint2(x0, y4)).yyz;
    color += inTexture.read(uint2(x2, y4)).xxx;
    color += inTexture.read(uint2(x1, y2)).zyy;
    color += inTexture.read(uint2(x4, y0)).zyz;
    color += inTexture.read(uint2(x2, y4)).zzz;
    color += inTexture.read(uint2(x0, y2)).zxz;
    color += inTexture.read(uint2(x1, y3)).xzx;
    color += inTexture.read(uint2(x2, y3)).zyz;
    color += inTexture.read(uint2(x1, y0)).zxz;
    color += inTexture.read(uint2(x4, y4)).zzx;
    color += inTexture.read(uint2(x4, y1)).zxx;
    color += inTexture.read(uint2(x0, y4)).zzz;
    color += inTexture.read(uint2(x1, y3)).yzx;
    color += inTexture.read(uint2(x3, y0)).xzz;
    color += inTexture.read(uint2(x4, y1)).yxy;
    color += inTexture.read(uint2(x2, y0)).yyy;
    color += inTexture.read(uint2(x4, y4)).xyz;
    color += inTexture.read(uint2(x2, y2)).yzx;
    color += inTexture.read(uint2(x2, y4)).zxz;
    color += inTexture.read(uint2(x0, y3)).zzx;
    color += inTexture.read(uint2(x3, y3)).xxx;
    color += inTexture.read(uint2(x1, y1)).xyz;
    color += inTexture.read(uint2(x1, y1)).zzx;
    color += inTexture.read(uint2(x0, y3)).xyy;
    color += inTexture.read(uint2(x0, y2)).yzy;
    color += inTexture.read(uint2(x0, y2)).yyy;
    color += inTexture.read(uint2(x4, y2)).yzx;
    color += inTexture.read(uint2(x2, y2)).zxz;
    color += inTexture.read(uint2(x1, y1)).xzx;
    color += inTexture.read(uint2(x4, y1)).zxz;
    color += inTexture.read(uint2(x4, y0)).zxy;
    color += inTexture.read(uint2(x3, y3)).zxy;
    color += inTexture.read(uint2(x3, y4)).zyy;
    color += inTexture.read(uint2(x4, y0)).zxy;
    color += inTexture.read(uint2(x4, y0)).xyx;
    color += inTexture.read(uint2(x3, y4)).yyz;
    color += inTexture.read(uint2(x4, y1)).xzx;
    color += inTexture.read(uint2(x2, y0)).xzy;
    color += inTexture.read(uint2(x3, y4)).yxy;
    color += inTexture.read(uint2(x1, y3)).xyx;
    color += inTexture.read(uint2(x3, y4)).yxy;
    color += inTexture.read(uint2(x4, y2)).xyz;
    color += inTexture.read(uint2(x3, y0)).yyx;
    color += inTexture.read(uint2(x1, y2)).yzx;
    color += inTexture.read(uint2(x4, y2)).zxz;
    color += inTexture.read(uint2(x2, y4)).xyz;
    color += inTexture.read(uint2(x4, y2)).yyz;
    color += inTexture.read(uint2(x0, y4)).xxx;
    color += inTexture.read(uint2(x3, y3)).xyy;
    color += inTexture.read(uint2(x4, y0)).zyy;
    color += inTexture.read(uint2(x3, y2)).yxx;
    color += inTexture.read(uint2(x1, y3)).yyy;
    color += inTexture.read(uint2(x2, y2)).zzx;
    color += inTexture.read(uint2(x1, y2)).yyy;
    color += inTexture.read(uint2(x3, y0)).zxx;
    color += inTexture.read(uint2(x0, y2)).xxz;
    color += inTexture.read(uint2(x4, y4)).zzz;
    color += inTexture.read(uint2(x0, y2)).xzx;
    color += inTexture.read(uint2(x0, y2)).xyx;
    color += inTexture.read(uint2(x0, y0)).yzz;
    color += inTexture.read(uint2(x4, y0)).xzz;
    color += inTexture.read(uint2(x2, y2)).zzz;
    color += inTexture.read(uint2(x3, y0)).yxz;
    color += inTexture.read(uint2(x0, y3)).yyz;
    color += inTexture.read(uint2(x4, y0)).zzz;
    color += inTexture.read(uint2(x0, y3)).zxy;
    color += inTexture.read(uint2(x3, y1)).yxx;
    color += inTexture.read(uint2(x2, y4)).zzx;
    color += inTexture.read(uint2(x3, y0)).xxx;
    color += inTexture.read(uint2(x0, y2)).zxz;
    color += inTexture.read(uint2(x2, y2)).zyy;
    color += inTexture.read(uint2(x0, y4)).zzx;
    color += inTexture.read(uint2(x1, y4)).yyx;
    color += inTexture.read(uint2(x4, y3)).xyy;
    color += inTexture.read(uint2(x0, y2)).xyx;
    color += inTexture.read(uint2(x0, y2)).xyz;
    color += inTexture.read(uint2(x3, y4)).zxz;
    color += inTexture.read(uint2(x2, y3)).zxx;
    color += inTexture.read(uint2(x0, y2)).yzx;
    color += inTexture.read(uint2(x3, y4)).yxy;
    color += inTexture.read(uint2(x4, y2)).xxx;
    color += inTexture.read(uint2(x0, y1)).yyx;
    color += inTexture.read(uint2(x2, y2)).xyx;
    color += inTexture.read(uint2(x3, y2)).yyx;
    color += inTexture.read(uint2(x2, y3)).zyx;
    color += inTexture.read(uint2(x1, y3)).zyy;
    color += inTexture.read(uint2(x2, y2)).zyx;
    color += inTexture.read(uint2(x3, y0)).yzz;
    color += inTexture.read(uint2(x4, y2)).yxz;
    color += inTexture.read(uint2(x3, y2)).xzy;
    color += inTexture.read(uint2(x3, y1)).zxy;
    color += inTexture.read(uint2(x4, y1)).yxy;
    color += inTexture.read(uint2(x3, y0)).xzy;
    color += inTexture.read(uint2(x1, y3)).zxx;
    color += inTexture.read(uint2(x2, y2)).yzz;
    color += inTexture.read(uint2(x0, y2)).zyy;
    color += inTexture.read(uint2(x4, y3)).zxy;
    color += inTexture.read(uint2(x2, y4)).xzx;
    color += inTexture.read(uint2(x1, y2)).zzy;
    color += inTexture.read(uint2(x1, y1)).yxz;
    color += inTexture.read(uint2(x0, y3)).yyx;
    color += inTexture.read(uint2(x3, y1)).xyz;
    color += inTexture.read(uint2(x0, y1)).yyy;
    color += inTexture.read(uint2(x0, y4)).xzz;
    color += inTexture.read(uint2(x0, y3)).xyz;
    color += inTexture.read(uint2(x4, y0)).xzy;
    color += inTexture.read(uint2(x0, y1)).zyy;
    color += inTexture.read(uint2(x4, y2)).yxx;
    color += inTexture.read(uint2(x1, y3)).xyy;
    color += inTexture.read(uint2(x3, y0)).zxy;
    color += inTexture.read(uint2(x3, y2)).xxz;
    color += inTexture.read(uint2(x1, y1)).yzy;
    color += inTexture.read(uint2(x1, y4)).zyx;
    color += inTexture.read(uint2(x2, y3)).yyx;
    color += inTexture.read(uint2(x1, y3)).yyy;
    color += inTexture.read(uint2(x2, y4)).yxy;
    color += inTexture.read(uint2(x1, y3)).xxx;
    color += inTexture.read(uint2(x0, y3)).yxx;
    color += inTexture.read(uint2(x2, y2)).xxx;
    color += inTexture.read(uint2(x3, y4)).yzy;
    color += inTexture.read(uint2(x2, y1)).xxy;
    color += inTexture.read(uint2(x2, y4)).yxy;
    color += inTexture.read(uint2(x0, y0)).zzz;
    color += inTexture.read(uint2(x1, y0)).yyy;
    color += inTexture.read(uint2(x3, y4)).yzx;
    color += inTexture.read(uint2(x2, y1)).zyy;
    color += inTexture.read(uint2(x2, y0)).zxy;
    color += inTexture.read(uint2(x1, y0)).yxx;
    color += inTexture.read(uint2(x1, y4)).xxy;
    color += inTexture.read(uint2(x4, y4)).xyx;
    color += inTexture.read(uint2(x0, y0)).yzx;
    color += inTexture.read(uint2(x1, y2)).zxx;
    color += inTexture.read(uint2(x2, y4)).yyy;
    color += inTexture.read(uint2(x3, y2)).yyz;
    color += inTexture.read(uint2(x3, y4)).yxx;
    color += inTexture.read(uint2(x2, y3)).zzy;
    color += inTexture.read(uint2(x4, y4)).zyx;
    color += inTexture.read(uint2(x3, y1)).zzy;
    color += inTexture.read(uint2(x0, y4)).xyx;
    color += inTexture.read(uint2(x4, y2)).yyx;
    color += inTexture.read(uint2(x1, y0)).yxy;
    color += inTexture.read(uint2(x2, y2)).xzy;
    color += inTexture.read(uint2(x3, y0)).xyx;
    color += inTexture.read(uint2(x3, y2)).yyx;
    color += inTexture.read(uint2(x1, y1)).zzz;
    color += inTexture.read(uint2(x0, y2)).zyz;
    color += inTexture.read(uint2(x4, y0)).yxx;
    color += inTexture.read(uint2(x2, y1)).xzy;
    color += inTexture.read(uint2(x2, y4)).zxz;
    color += inTexture.read(uint2(x2, y1)).yyx;
    color += inTexture.read(uint2(x2, y4)).yxz;
    color += inTexture.read(uint2(x2, y0)).zzx;
    color += inTexture.read(uint2(x2, y3)).yyx;
    color += inTexture.read(uint2(x4, y3)).zyy;
    color += inTexture.read(uint2(x4, y4)).zyx;
    color += inTexture.read(uint2(x0, y4)).zyx;
    color += inTexture.read(uint2(x1, y0)).zzx;
    color += inTexture.read(uint2(x3, y0)).xyz;
    color += inTexture.read(uint2(x1, y3)).yxx;
    color += inTexture.read(uint2(x2, y2)).yxy;
    color += inTexture.read(uint2(x0, y3)).zxy;
    color += inTexture.read(uint2(x0, y1)).yxy;
    color += inTexture.read(uint2(x3, y1)).xzy;
    color += inTexture.read(uint2(x1, y1)).yzz;
    color += inTexture.read(uint2(x3, y4)).xzx;
    color += inTexture.read(uint2(x0, y3)).yyy;
    color += inTexture.read(uint2(x0, y0)).xyx;
    color += inTexture.read(uint2(x2, y0)).zyx;
    color += inTexture.read(uint2(x4, y3)).xxy;
    color += inTexture.read(uint2(x4, y0)).zxy;
    color += inTexture.read(uint2(x1, y1)).yyx;
    color += inTexture.read(uint2(x0, y1)).zyx;
    color += inTexture.read(uint2(x1, y4)).yzx;
    color += inTexture.read(uint2(x2, y0)).zzy;
    color += inTexture.read(uint2(x0, y2)).xzy;
    color += inTexture.read(uint2(x0, y2)).yxx;
    color += inTexture.read(uint2(x4, y2)).xxy;
    color += inTexture.read(uint2(x3, y2)).yzx;
    color += inTexture.read(uint2(x1, y3)).yxx;
    color += inTexture.read(uint2(x1, y1)).yyz;
    color += inTexture.read(uint2(x3, y2)).xzy;
    color += inTexture.read(uint2(x1, y2)).yzy;
    color += inTexture.read(uint2(x0, y1)).zzz;
    color += inTexture.read(uint2(x3, y1)).zyz;
    color += inTexture.read(uint2(x0, y2)).xxz;
    color += inTexture.read(uint2(x3, y0)).zyy;
    color += inTexture.read(uint2(x0, y1)).xzy;
    color += inTexture.read(uint2(x0, y2)).xyz;
    color += inTexture.read(uint2(x2, y0)).yyy;
    color += inTexture.read(uint2(x0, y1)).xxx;
    color += inTexture.read(uint2(x2, y1)).yyy;
    color += inTexture.read(uint2(x0, y1)).xxx;
    color += inTexture.read(uint2(x4, y4)).zyz;
    color += inTexture.read(uint2(x0, y2)).yzy;
    color += inTexture.read(uint2(x2, y3)).xzy;
    color += inTexture.read(uint2(x3, y4)).yyx;
    color += inTexture.read(uint2(x0, y3)).zyz;
    color += inTexture.read(uint2(x2, y0)).yyy;
    color += inTexture.read(uint2(x2, y2)).yyy;
    color += inTexture.read(uint2(x4, y3)).xxz;
    color += inTexture.read(uint2(x1, y1)).zyz;
    color += inTexture.read(uint2(x1, y0)).yzx;
    color += inTexture.read(uint2(x0, y4)).yxx;
    color += inTexture.read(uint2(x0, y2)).xyz;
    color += inTexture.read(uint2(x2, y4)).zzx;
    color += inTexture.read(uint2(x0, y3)).xxy;
    color += inTexture.read(uint2(x3, y0)).xzx;
    color += inTexture.read(uint2(x3, y3)).xxy;
    color += inTexture.read(uint2(x2, y0)).zxy;
    color += inTexture.read(uint2(x2, y0)).zzy;
    color += inTexture.read(uint2(x0, y1)).zxx;
    color += inTexture.read(uint2(x2, y2)).yzx;
    color += inTexture.read(uint2(x2, y4)).zyy;
    color += inTexture.read(uint2(x4, y2)).xzy;
    color += inTexture.read(uint2(x1, y0)).zyy;
    color += inTexture.read(uint2(x0, y4)).yxz;
    color += inTexture.read(uint2(x4, y4)).yxy;
    color += inTexture.read(uint2(x0, y0)).xzy;
    color += inTexture.read(uint2(x0, y1)).zyz;
    color += inTexture.read(uint2(x1, y1)).zxy;
    color += inTexture.read(uint2(x2, y2)).zzy;
    color += inTexture.read(uint2(x3, y2)).xyz;
    color += inTexture.read(uint2(x3, y2)).zyx;
    color += inTexture.read(uint2(x2, y4)).xzx;
    color += inTexture.read(uint2(x1, y3)).yyz;
    color += inTexture.read(uint2(x3, y4)).yzz;
    color += inTexture.read(uint2(x2, y0)).yyx;
    color += inTexture.read(uint2(x2, y3)).zzy;
    color += inTexture.read(uint2(x3, y3)).yzy;
    color += inTexture.read(uint2(x2, y0)).zyz;
    color += inTexture.read(uint2(x0, y4)).yzz;
    color += inTexture.read(uint2(x1, y3)).xzz;
    color += inTexture.read(uint2(x3, y1)).yzy;
    color += inTexture.read(uint2(x2, y4)).yzy;
    color += inTexture.read(uint2(x2, y2)).zzz;
    color += inTexture.read(uint2(x0, y3)).zxx;
    color += inTexture.read(uint2(x2, y1)).xyy;
    color += inTexture.read(uint2(x3, y1)).xzz;
    color += inTexture.read(uint2(x3, y2)).xyx;
    color += inTexture.read(uint2(x2, y4)).xxx;
    color += inTexture.read(uint2(x0, y0)).xyy;
    color += inTexture.read(uint2(x3, y4)).zxy;
    color += inTexture.read(uint2(x4, y0)).xzx;
    color += inTexture.read(uint2(x2, y2)).zxx;
    color += inTexture.read(uint2(x4, y0)).zyx;
    color += inTexture.read(uint2(x1, y3)).zxz;
    color += inTexture.read(uint2(x4, y1)).yxy;
    color += inTexture.read(uint2(x4, y0)).xzx;
    color += inTexture.read(uint2(x2, y1)).xyx;
    color += inTexture.read(uint2(x3, y1)).xzz;
    color += inTexture.read(uint2(x4, y4)).xyz;
    color += inTexture.read(uint2(x1, y3)).zxx;
    color += inTexture.read(uint2(x2, y4)).xzx;
    color += inTexture.read(uint2(x3, y1)).xyz;
    color += inTexture.read(uint2(x2, y1)).zyz;
    color += inTexture.read(uint2(x3, y0)).yxx;
    color += inTexture.read(uint2(x1, y1)).xyy;
    color += inTexture.read(uint2(x4, y1)).zzy;
    color += inTexture.read(uint2(x3, y1)).xxy;
    color += inTexture.read(uint2(x4, y3)).zxy;
    color += inTexture.read(uint2(x1, y3)).xzy;
    color += inTexture.read(uint2(x3, y3)).zyx;
    color += inTexture.read(uint2(x4, y2)).xzx;
    color += inTexture.read(uint2(x4, y3)).xzx;
    color += inTexture.read(uint2(x1, y3)).xzx;
    color += inTexture.read(uint2(x1, y1)).zyz;
    color += inTexture.read(uint2(x2, y4)).xxz;
    color += inTexture.read(uint2(x3, y4)).xyx;
    color += inTexture.read(uint2(x0, y0)).xyz;
    color += inTexture.read(uint2(x1, y4)).yyx;
    color += inTexture.read(uint2(x2, y3)).zxz;
    color += inTexture.read(uint2(x2, y4)).zzy;
    color += inTexture.read(uint2(x3, y2)).zzz;
    color += inTexture.read(uint2(x0, y3)).yxx;
    color += inTexture.read(uint2(x2, y0)).xxx;
    color += inTexture.read(uint2(x0, y3)).yzx;
    color += inTexture.read(uint2(x3, y0)).xzx;
    color += inTexture.read(uint2(x0, y2)).yyx;
    color += inTexture.read(uint2(x1, y0)).zzx;
    color += inTexture.read(uint2(x0, y0)).xyx;
    color += inTexture.read(uint2(x2, y4)).yzz;
    color += inTexture.read(uint2(x4, y0)).xyz;
    color += inTexture.read(uint2(x1, y0)).zxx;
    color += inTexture.read(uint2(x4, y0)).zzx;
    color += inTexture.read(uint2(x4, y2)).zyy;
    color += inTexture.read(uint2(x1, y1)).zzz;
    color += inTexture.read(uint2(x0, y4)).zxz;
    color += inTexture.read(uint2(x3, y4)).zyx;
    color += inTexture.read(uint2(x4, y1)).zyz;
    color += inTexture.read(uint2(x0, y1)).xxz;
    color += inTexture.read(uint2(x4, y2)).yxx;
    color += inTexture.read(uint2(x4, y3)).zzy;
    color += inTexture.read(uint2(x2, y2)).yxx;
    color += inTexture.read(uint2(x4, y1)).xyy;
    color += inTexture.read(uint2(x0, y1)).xzz;
    color += inTexture.read(uint2(x0, y0)).xyz;
    color += inTexture.read(uint2(x0, y4)).zyx;
    color += inTexture.read(uint2(x1, y3)).yzy;
    color += inTexture.read(uint2(x2, y0)).zyy;
    color += inTexture.read(uint2(x3, y4)).xzz;
    color += inTexture.read(uint2(x0, y3)).xyx;
    color += inTexture.read(uint2(x1, y2)).xzy;
    color += inTexture.read(uint2(x4, y0)).yzz;
    color += inTexture.read(uint2(x0, y0)).yzy;
    color += inTexture.read(uint2(x4, y3)).yyx;
    color += inTexture.read(uint2(x0, y2)).zzy;
    color += inTexture.read(uint2(x2, y4)).xzx;
    color += inTexture.read(uint2(x1, y2)).xyx;
    color += inTexture.read(uint2(x2, y2)).yxx;
    color += inTexture.read(uint2(x4, y1)).yyx;
    color += inTexture.read(uint2(x1, y2)).xxx;
    color += inTexture.read(uint2(x1, y0)).yzy;
    color += inTexture.read(uint2(x2, y3)).zxx;
    color += inTexture.read(uint2(x3, y0)).yzz;
    color += inTexture.read(uint2(x1, y2)).yyx;
    color += inTexture.read(uint2(x3, y2)).yxy;
    color += inTexture.read(uint2(x2, y0)).zxx;
    color += inTexture.read(uint2(x3, y4)).yyx;
    color += inTexture.read(uint2(x0, y0)).zxz;
    color += inTexture.read(uint2(x2, y0)).zyx;
    color += inTexture.read(uint2(x2, y2)).yxx;
    color += inTexture.read(uint2(x2, y2)).yyy;
    color += inTexture.read(uint2(x2, y2)).yxx;
    color += inTexture.read(uint2(x0, y4)).xzx;
    color += inTexture.read(uint2(x3, y0)).yzy;
    color += inTexture.read(uint2(x0, y2)).yzz;
    color += inTexture.read(uint2(x4, y4)).xyy;
    color += inTexture.read(uint2(x1, y0)).zxy;
    color += inTexture.read(uint2(x4, y3)).yzx;
    color += inTexture.read(uint2(x0, y2)).xxx;
    color += inTexture.read(uint2(x0, y1)).yyy;
    color += inTexture.read(uint2(x2, y4)).yzx;
    color += inTexture.read(uint2(x2, y0)).yxx;
    color += inTexture.read(uint2(x4, y2)).xxx;
    color += inTexture.read(uint2(x4, y1)).xzz;
    color += inTexture.read(uint2(x2, y3)).yzx;
    color += inTexture.read(uint2(x1, y1)).zyx;
    color += inTexture.read(uint2(x1, y0)).yxx;
    color += inTexture.read(uint2(x1, y4)).zxx;
    color += inTexture.read(uint2(x4, y3)).zxz;
    color += inTexture.read(uint2(x3, y3)).xzy;
    color += inTexture.read(uint2(x4, y2)).xxy;
    color += inTexture.read(uint2(x4, y2)).xzy;
    color += inTexture.read(uint2(x3, y0)).xzx;
    color += inTexture.read(uint2(x2, y2)).zyz;
    color += inTexture.read(uint2(x3, y0)).yyz;
    color += inTexture.read(uint2(x0, y3)).yzx;
    color += inTexture.read(uint2(x1, y0)).zxx;
    color += inTexture.read(uint2(x0, y4)).xxy;
    color += inTexture.read(uint2(x3, y0)).yzy;
    color += inTexture.read(uint2(x1, y3)).zxx;
    color += inTexture.read(uint2(x0, y1)).xxz;
    color += inTexture.read(uint2(x4, y0)).zxy;
    color += inTexture.read(uint2(x0, y3)).zyx;
    color += inTexture.read(uint2(x2, y3)).yyx;
    color += inTexture.read(uint2(x4, y3)).zxz;
    color += inTexture.read(uint2(x3, y2)).yxy;
    color += inTexture.read(uint2(x3, y1)).zxx;
    color += inTexture.read(uint2(x0, y3)).yzz;
    color += inTexture.read(uint2(x3, y4)).xzx;
    color += inTexture.read(uint2(x0, y1)).yzz;
    color += inTexture.read(uint2(x3, y2)).xyy;
    color += inTexture.read(uint2(x1, y0)).zyx;
    color += inTexture.read(uint2(x4, y4)).xxx;
    color += inTexture.read(uint2(x2, y4)).zyy;
    color += inTexture.read(uint2(x3, y1)).xyx;
    color += inTexture.read(uint2(x2, y3)).yyx;
    color += inTexture.read(uint2(x4, y3)).xxz;
    color += inTexture.read(uint2(x1, y4)).zyx;
    color += inTexture.read(uint2(x3, y1)).xzz;
    color += inTexture.read(uint2(x1, y1)).yyx;
    color += inTexture.read(uint2(x1, y4)).zxz;
    color += inTexture.read(uint2(x1, y0)).zyy;
    color += inTexture.read(uint2(x2, y0)).zzz;
    color += inTexture.read(uint2(x1, y2)).zzx;
    color += inTexture.read(uint2(x1, y4)).xxz;
    color += inTexture.read(uint2(x3, y3)).zxy;
    color += inTexture.read(uint2(x0, y4)).zyz;
    color += inTexture.read(uint2(x0, y4)).xzy;
    color += inTexture.read(uint2(x1, y4)).zxy;
    color += inTexture.read(uint2(x1, y3)).zxx;
    color += inTexture.read(uint2(x3, y3)).zyy;
    color += inTexture.read(uint2(x1, y0)).yyx;
    color += inTexture.read(uint2(x4, y2)).xzy;
    color += inTexture.read(uint2(x0, y2)).yxx;
    color += inTexture.read(uint2(x2, y0)).zzx;
    color += inTexture.read(uint2(x4, y4)).xzz;
    color += inTexture.read(uint2(x0, y3)).xyy;
    color += inTexture.read(uint2(x0, y3)).xxy;
    color += inTexture.read(uint2(x0, y4)).zxz;
    color += inTexture.read(uint2(x4, y4)).xyy;
    color += inTexture.read(uint2(x3, y1)).xxz;
    color += inTexture.read(uint2(x2, y4)).zzz;
    color += inTexture.read(uint2(x1, y1)).xxx;
    color += inTexture.read(uint2(x3, y3)).yyx;
    color += inTexture.read(uint2(x2, y3)).yxx;
    color += inTexture.read(uint2(x2, y3)).zzy;
    color += inTexture.read(uint2(x1, y2)).xxz;
    color += inTexture.read(uint2(x2, y4)).yxy;
    color += inTexture.read(uint2(x2, y2)).zyy;
    color += inTexture.read(uint2(x2, y1)).xzx;
    color += inTexture.read(uint2(x1, y2)).zzz;
    color += inTexture.read(uint2(x2, y0)).zzz;
    color += inTexture.read(uint2(x2, y4)).yzx;
    color += inTexture.read(uint2(x2, y4)).yzz;
    color += inTexture.read(uint2(x2, y2)).xzx;
    color += inTexture.read(uint2(x2, y1)).zyy;
    color += inTexture.read(uint2(x0, y0)).zxy;
    color += inTexture.read(uint2(x2, y4)).xyx;
    color += inTexture.read(uint2(x1, y2)).yyx;
    color += inTexture.read(uint2(x3, y3)).zyz;
    color += inTexture.read(uint2(x0, y0)).yyy;
    color += inTexture.read(uint2(x1, y4)).xzz;
    color += inTexture.read(uint2(x4, y3)).zxx;
    color += inTexture.read(uint2(x4, y0)).zzy;
    color += inTexture.read(uint2(x4, y0)).xzx;
    color += inTexture.read(uint2(x3, y1)).yxz;
    color += inTexture.read(uint2(x3, y1)).yzz;
    color += inTexture.read(uint2(x4, y0)).zyy;
    color += inTexture.read(uint2(x2, y2)).xzx;
    color += inTexture.read(uint2(x0, y2)).zzy;
    color += inTexture.read(uint2(x0, y3)).xyy;
    color += inTexture.read(uint2(x2, y3)).zyz;
    color += inTexture.read(uint2(x3, y3)).yzy;
    color += inTexture.read(uint2(x4, y3)).zxz;
    color += inTexture.read(uint2(x4, y2)).yyy;
    color += inTexture.read(uint2(x3, y1)).zxy;
    color += inTexture.read(uint2(x4, y4)).zzx;
    color += inTexture.read(uint2(x0, y4)).zxy;
    color += inTexture.read(uint2(x4, y2)).zzy;
    color += inTexture.read(uint2(x0, y2)).zyz;
    color += inTexture.read(uint2(x4, y3)).zyz;
    color += inTexture.read(uint2(x1, y1)).xxx;
    color += inTexture.read(uint2(x2, y2)).yzz;
    color += inTexture.read(uint2(x0, y4)).yzz;
    color += inTexture.read(uint2(x1, y2)).zzx;
    color += inTexture.read(uint2(x4, y3)).zzy;
    color += inTexture.read(uint2(x1, y4)).yzx;
    color += inTexture.read(uint2(x3, y0)).yxy;
    color += inTexture.read(uint2(x2, y3)).yzy;
    color += inTexture.read(uint2(x2, y0)).zzx;
    color += inTexture.read(uint2(x1, y3)).zzy;
    color += inTexture.read(uint2(x1, y2)).yxx;
    color += inTexture.read(uint2(x0, y4)).xzy;
    color += inTexture.read(uint2(x3, y0)).xyz;
    color += inTexture.read(uint2(x2, y0)).zxx;
    color += inTexture.read(uint2(x0, y0)).zxy;
    color += inTexture.read(uint2(x4, y0)).yyx;
    color += inTexture.read(uint2(x2, y1)).zxy;
    color += inTexture.read(uint2(x2, y1)).xyz;
    color += inTexture.read(uint2(x0, y2)).xxy;
    color += inTexture.read(uint2(x3, y0)).zzz;
    color += inTexture.read(uint2(x1, y3)).yxx;
    color += inTexture.read(uint2(x1, y3)).yyy;
    color += inTexture.read(uint2(x1, y2)).yyx;
    color += inTexture.read(uint2(x0, y0)).xzy;
    color += inTexture.read(uint2(x4, y1)).zxz;
    color += inTexture.read(uint2(x4, y3)).zxz;
    color += inTexture.read(uint2(x3, y3)).yzz;
    color += inTexture.read(uint2(x3, y2)).xzx;
    color += inTexture.read(uint2(x3, y3)).yyz;
    color += inTexture.read(uint2(x4, y1)).zzz;
    color += inTexture.read(uint2(x0, y0)).xxx;
    color += inTexture.read(uint2(x4, y0)).xxy;
    color += inTexture.read(uint2(x4, y3)).yyz;
    color += inTexture.read(uint2(x0, y1)).xxz;
    color += inTexture.read(uint2(x2, y1)).xyz;
    color += inTexture.read(uint2(x1, y2)).zxy;
    color += inTexture.read(uint2(x3, y3)).zyx;
    color += inTexture.read(uint2(x4, y3)).xyy;
    color += inTexture.read(uint2(x3, y2)).xzy;
    color += inTexture.read(uint2(x2, y4)).yzy;
    color += inTexture.read(uint2(x3, y2)).yxx;
    color += inTexture.read(uint2(x4, y4)).xyz;
    color += inTexture.read(uint2(x4, y2)).yzz;
    color += inTexture.read(uint2(x2, y4)).zxy;
    color += inTexture.read(uint2(x3, y2)).zyy;
    color += inTexture.read(uint2(x1, y4)).yzx;
    color += inTexture.read(uint2(x3, y1)).xyy;
    color += inTexture.read(uint2(x1, y4)).xyz;
    color += inTexture.read(uint2(x3, y2)).xxx;
    color += inTexture.read(uint2(x0, y2)).yzx;
    color += inTexture.read(uint2(x3, y2)).xzz;
    color += inTexture.read(uint2(x2, y4)).zxz;
    color = color / 500.0;
    
    outTexture.write(float4(color, 0.13337), gid);
}
```

这道题和上一道不同，光有shader代码还不能解题，我们还需要再分析二进制文件Bytal，ida打开

~~暂时还不知道怎么~~定位到-[MBEViewController poorSuddenI]函数

一般在一个项目中定义一个**MBEViewController.m**文件

在xcode工程中

.m：源代码文件。这是典型的源代码文件扩展名，可以包含Objective-C和C代码。

.mm：源代码文件。带有这种扩展名的源代码文件，除了可以包含Objective-C和C代码以外还可以包含C++代码。仅在Objective-C代码中确实需要使用C++类或者特性的时候才用这种扩展名

-[MBEViewController poorSuddenI]

```assembly
void __cdecl -[MBEViewController poorSuddenI](MBEViewController *self, SEL a2)
{
  char *v3; // x0
  id v4; // x20
  id v5; // x0
  NSObject *v6; // x21
  __int64 v7[6]; // [xsp+0h] [xbp-50h] BYREF

  v3 = -[MBEViewController copyOnly](self, "copyOnly");
  -[MBEViewController setCopyOnly:](self, "setCopyOnly:", v3 + 1);
  v4 = -[MBEViewController copyOnly](self, "copyOnly");
  v5 = -[MBEViewController natureShareLet](self, "natureShareLet");
  v6 = objc_retainAutoreleasedReturnValue(v5);
  v7[0] = (__int64)_NSConcreteStackBlock;
  v7[1] = 0xC2000000LL;
  v7[2] = (__int64)sub_1000065D8;
  v7[3] = (__int64)&unk_10000C088;
  v7[4] = (__int64)self;
  v7[5] = (__int64)v4;
  dispatch_async(v6, v7);
  objc_release(v6);
}
```

sub_1000065D8

```assembly
void __fastcall sub_1000065D8(__int64 a1)
{
  id v2; // x20
  id v3; // x0
  id v4; // x21
  id v5; // x0
  id v6; // x20
  id v7; // x0
  __int64 v8; // x8
  __int64 v9[4]; // [xsp+0h] [xbp-50h] BYREF
  id v10; // [xsp+20h] [xbp-30h]
  __int64 v11; // [xsp+28h] [xbp-28h]

  v2 = *(id *)(a1 + 0x28);
  if ( v2 == objc_msgSend(*(id *)(a1 + 0x20), "copyOnly") )
  {
    v3 = objc_msgSend(*(id *)(a1 + 0x20), "seeViewBell");
    v4 = objc_retainAutoreleasedReturnValue(v3);
    v5 = objc_msgSend(v4, "texture");
    v6 = objc_retainAutoreleasedReturnValue(v5);
    objc_release(v4);
    if ( v6 )
    {
      v9[0] = (__int64)_NSConcreteStackBlock;
      v9[1] = 0xC2000000LL;
      v9[2] = (__int64)sub_1000066D0;
      v9[3] = (__int64)&unk_10000C058;
      v7 = objc_retain(v6);
      v8 = *(_QWORD *)(a1 + 0x20);
      v10 = v7;
      v11 = v8;
      dispatch_async((dispatch_queue_t)&_dispatch_main_q, v9);
      objc_release(v10);
    }
    objc_release(v6);
  }
}
```

sub_1000066D0

```assembly
void __fastcall sub_1000066D0(__int64 a1)
{
  CIContext *v2; // x0
  CIImage *v3; // x0
  CIImage *v4; // x20
  id v5; // x19
  id v6; // x0
  CGImage *v7; // x25
  unsigned __int64 v8; // x26
  unsigned __int64 v9; // x27
  CGColorSpace *v10; // x28
  void *v11; // x24
  CGContext *v12; // x19
  unsigned __int64 v13; // x25
  id v14; // x19
  unsigned int v15; // s0
  float v16; // s0
  CIContext *v17; // [xsp+8h] [xbp-68h]
  CGRect v18; // 0:d0.8,8:d1.8,16:d2.8,24:d3.8

  v2 = objc_msgSend(&OBJC_CLASS___CIContext, "contextWithOptions:", 0LL);
  v17 = objc_retainAutoreleasedReturnValue(v2);
  v3 = objc_msgSend(&OBJC_CLASS___CIImage, "imageWithMTLTexture:options:", *(_QWORD *)(a1 + 0x20), 0LL);
  v4 = objc_retainAutoreleasedReturnValue(v3);
  v5 = objc_msgSend(*(id *)(a1 + 0x20), "width");
  v6 = objc_msgSend(*(id *)(a1 + 0x20), "height");
  v7 = (CGImage *)objc_msgSend(
                    v17,
                    "createCGImage:fromRect:format:colorSpace:",
                    v4,
                    (unsigned int)kCIFormatABGR8,
                    0LL,
                    0.0,
                    0.0,
                    (double)(unsigned __int64)v5,
                    (double)(unsigned __int64)v6);
  v8 = CGImageGetWidth(v7);
  v9 = CGImageGetHeight(v7);
  v10 = CGColorSpaceCreateDeviceRGB();
  v11 = calloc(4 * v8 * v9, 1uLL);
  v12 = CGBitmapContextCreate(v11, v8, v9, 8uLL, 4 * v8, v10, 0x2001u);
  CGColorSpaceRelease(v10);
  v18.size.width = (double)v8;
  v18.size.height = (double)v9;
  v18.origin.x = 0.0;
  v18.origin.y = 0.0;
  CGContextDrawImage(v12, v18, v7);
  CGContextRelease(v12);
  v13 = 0LL;
  while ( 1 )
  {
    v14 = objc_msgSend(*(id *)(a1 + 0x20), "width");
    if ( v13 > 4LL * (_QWORD)v14 * (_QWORD)objc_msgSend(*(id *)(a1 + 0x20), "height") )
      break;
    LOBYTE(v15) = *((_BYTE *)v11 + v13);
    v16 = vabds_f32((float)v15, flt_10000B720[v13++]);
    if ( v16 > 1.0 )
    {
      objc_msgSend(*(id *)(a1 + 0x28), "car");
      goto LABEL_6;
    }
  }
  objc_msgSend(*(id *)(a1 + 0x28), "he");
LABEL_6:
  free(v11);
  objc_release(v4);
  objc_release(v17);
}
```

flt_10000B720

```assembly
__const:000000010000B720 ; float flt_10000B720[324]
__const:000000010000B720 flt_10000B720   DCFS 34.01, 58.83, 57.726, 60.162, 34.01, 60.89, 62.206
__const:000000010000B720                                         ; DATA XREF: sub_1000066D0+15C↑o
__const:000000010000B720                 DCFS 59.312, 34.01, 63.328, 62.97, 62.592, 34.01, 59.616
__const:000000010000B720                 DCFS 56.748, 57.018, 34.01, 63.448, 62.144, 59.942, 34.01
__const:000000010000B720                 DCFS 59.294, 56.5, 56.262, 34.01, 56.992, 55.134, 54.712
__const:000000010000B720                 DCFS 34.01, 58.776, 58.55, 55.268, 34.01, 62.102, 63.294
__const:000000010000B720                 DCFS 64.81, 34.01, 57.446, 59.01, 56.574, 34.01, 58.718
__const:000000010000B720                 DCFS 59.928, 58.292, 34.01, 60.072, 59.508, 60.914, 34.01
__const:000000010000B720                 DCFS 57.948, 54.538, 54.27, 34.01, 59.496, 58.018, 54.868
__const:000000010000B720                 DCFS 34.01, 56.11, 56.284, 58.23, 34.01, 53.614, 51.836
__const:000000010000B720                 DCFS 54.016, 34.01, 57.512, 55.182, 54.416, 34.01, 55.144
__const:000000010000B720                 DCFS 56.52, 59.55, 34.01, 52.722, 52.568, 50.42, 34.01
__const:000000010000B720                 DCFS 55.524, 55.796, 56.034, 34.01, 54.752, 54.758, 55.564
__const:000000010000B720                 DCFS 34.01, 54.824, 56.42, 55.944, 34.01, 53.486, 55.722
__const:000000010000B720                 DCFS 52.85, 34.01, 54.074, 52.38, 55.884, 34.01, 52.29
__const:000000010000B720                 DCFS 50.39, 47.584, 34.01, 50.45, 51.694, 50.442, 34.01
__const:000000010000B720                 DCFS 51.54, 52.34, 55.244, 34.01, 43.204, 44.668, 43.558
__const:000000010000B720                 DCFS 34.01, 46.584, 46.85, 47.628, 34.01, 46.822, 46.208
__const:000000010000B720                 DCFS 47.286, 34.01, 46.418, 46.772, 46.944, 34.01, 45.786
__const:000000010000B720                 DCFS 46.854, 45.322, 34.01, 43.518, 43.836, 44.854, 34.01
__const:000000010000B720                 DCFS 44.226, 43.148, 42.18, 34.01, 44.192, 43.506, 41.21
__const:000000010000B720                 DCFS 34.01, 43.17, 43.008, 44.632, 34.01, 33.356, 35.692
__const:000000010000B720                 DCFS 35.36, 34.01, 37.01, 38.258, 37.848, 34.01, 37.322
__const:000000010000B720                 DCFS 36.962, 35.21, 34.01, 42.966, 43.968, 42.78, 34.01
__const:000000010000B720                 DCFS 39.914, 38.01, 37.956, 34.01, 40.59, 40.49, 41.182
__const:000000010000B720                 DCFS 34.01, 34.376, 35.552, 33.306, 34.01, 32.912, 33.084
__const:000000010000B720                 DCFS 34.376, 34.01, 33.232, 34.094, 34.64, 34.01, 30.378
__const:000000010000B720                 DCFS 30.54, 32.712, 34.01, 36.564, 36.046, 33.074, 34.01
__const:000000010000B720                 DCFS 33.736, 33.838, 36.35, 34.01, 35.67, 34.892, 36.04
__const:000000010000B720                 DCFS 34.01, 37.022, 36.984, 35.984, 34.01, 37.022, 36.384
__const:000000010000B720                 DCFS 37.066, 34.01, 35.51, 35.852, 35.916, 34.01, 32.308
__const:000000010000B720                 DCFS 31.382, 31.968, 34.01, 30.776, 32.55, 33.134, 34.01
__const:000000010000B720                 DCFS 34.046, 36.01, 35.812, 34.01, 33.246, 32.846, 34.038
__const:000000010000B720                 DCFS 34.01, 35.638, 35.918, 36.54, 34.01, 39.526, 37.942
__const:000000010000B720                 DCFS 38.924, 34.01, 36.85, 35.348, 36.616, 34.01, 41.588
__const:000000010000B720                 DCFS 42.608, 40.312, 34.01, 34.12, 34.518, 34.748, 34.01
__const:000000010000B720                 DCFS 33.84, 33.494, 34.338, 34.01, 30.966, 32.548, 31.798
__const:000000010000B720                 DCFS 34.01, 44.652, 45.188, 47.53, 34.01, 47.268, 45.81
__const:000000010000B720                 DCFS 48.986, 34.01, 49.218, 48.02, 47.092, 34.01, 46.148
__const:000000010000B720                 DCFS 44.744, 45.818, 34.01, 50.2, 49.81, 48.574, 34.01
__const:000000010000B720                 DCFS 44.778, 45.224, 45.116, 34.01, 44.568, 43.856, 46.386
__const:000000010000B720                 DCFS 34.01, 45.63, 45.61, 45.186, 34.01, 48.958, 50.86
__const:000000010000B720                 DCFS 50.526, 34.01, 50.626, 50.004, 51.126, 34.01, 51.026
__const:000000010000B720                 DCFS 49.298, 50.144, 34.01, 53.058, 53.048, 50.668, 34.01
__const:000000010000B720                 DCFS 48.976, 49.48, 50.014, 34.01, 54.53, 51.056, 51.992
__const:000000010000B720                 DCFS 34.01, 55.73, 54.01, 51.102, 34.01, 50.078, 47.868
__const:000000010000B720                 DCFS 48.632, 34.01, 51.714, 51.55, 49.202, 34.01, 49.916
__const:000000010000B720                 DCFS 50.724, 48.774
```

vabds_f32

Floating-point Absolute Difference (vector). This instruction subtracts the floating-point values in the elements of the second source SIMD&FP register, from the corresponding floating-point values in the elements of the first source SIMD&FP register, places the absolute value of each result in a vector, and writes the vector to the destination SIMD&FP register.This instruction can generate a floating-point exception.

解题脚本

```assembly
import numpy as np
import imageio

np.set_printoptions(suppress=True)

code = """
color += inTexture.read(uint2(x4, y4)).xxy;
color += inTexture.read(uint2(x2, y1)).zzz;
color += inTexture.read(uint2(x4, y1)).zzx;
color += inTexture.read(uint2(x1, y3)).zyx;
color += inTexture.read(uint2(x3, y2)).zyy;
color += inTexture.read(uint2(x0, y4)).yyx;
color += inTexture.read(uint2(x4, y0)).xzz;
color += inTexture.read(uint2(x4, y0)).zxy;
color += inTexture.read(uint2(x4, y2)).xxz;
color += inTexture.read(uint2(x3, y4)).xyx;
color += inTexture.read(uint2(x0, y4)).zzx;
color += inTexture.read(uint2(x3, y4)).yxx;
color += inTexture.read(uint2(x4, y4)).zzx;
color += inTexture.read(uint2(x2, y1)).yyz;
color += inTexture.read(uint2(x3, y0)).yyy;
color += inTexture.read(uint2(x1, y3)).yxz;
color += inTexture.read(uint2(x0, y4)).yyz;
color += inTexture.read(uint2(x2, y4)).xxx;
color += inTexture.read(uint2(x1, y2)).zyy;
color += inTexture.read(uint2(x4, y0)).zyz;
color += inTexture.read(uint2(x2, y4)).zzz;
color += inTexture.read(uint2(x0, y2)).zxz;
color += inTexture.read(uint2(x1, y3)).xzx;
color += inTexture.read(uint2(x2, y3)).zyz;
color += inTexture.read(uint2(x1, y0)).zxz;
color += inTexture.read(uint2(x4, y4)).zzx;
color += inTexture.read(uint2(x4, y1)).zxx;
color += inTexture.read(uint2(x0, y4)).zzz;
color += inTexture.read(uint2(x1, y3)).yzx;
color += inTexture.read(uint2(x3, y0)).xzz;
color += inTexture.read(uint2(x4, y1)).yxy;
color += inTexture.read(uint2(x2, y0)).yyy;
color += inTexture.read(uint2(x4, y4)).xyz;
color += inTexture.read(uint2(x2, y2)).yzx;
color += inTexture.read(uint2(x2, y4)).zxz;
color += inTexture.read(uint2(x0, y3)).zzx;
color += inTexture.read(uint2(x3, y3)).xxx;
color += inTexture.read(uint2(x1, y1)).xyz;
color += inTexture.read(uint2(x1, y1)).zzx;
color += inTexture.read(uint2(x0, y3)).xyy;
color += inTexture.read(uint2(x0, y2)).yzy;
color += inTexture.read(uint2(x0, y2)).yyy;
color += inTexture.read(uint2(x4, y2)).yzx;
color += inTexture.read(uint2(x2, y2)).zxz;
color += inTexture.read(uint2(x1, y1)).xzx;
color += inTexture.read(uint2(x4, y1)).zxz;
color += inTexture.read(uint2(x4, y0)).zxy;
color += inTexture.read(uint2(x3, y3)).zxy;
color += inTexture.read(uint2(x3, y4)).zyy;
color += inTexture.read(uint2(x4, y0)).zxy;
color += inTexture.read(uint2(x4, y0)).xyx;
color += inTexture.read(uint2(x3, y4)).yyz;
color += inTexture.read(uint2(x4, y1)).xzx;
color += inTexture.read(uint2(x2, y0)).xzy;
color += inTexture.read(uint2(x3, y4)).yxy;
color += inTexture.read(uint2(x1, y3)).xyx;
color += inTexture.read(uint2(x3, y4)).yxy;
color += inTexture.read(uint2(x4, y2)).xyz;
color += inTexture.read(uint2(x3, y0)).yyx;
color += inTexture.read(uint2(x1, y2)).yzx;
color += inTexture.read(uint2(x4, y2)).zxz;
color += inTexture.read(uint2(x2, y4)).xyz;
color += inTexture.read(uint2(x4, y2)).yyz;
color += inTexture.read(uint2(x0, y4)).xxx;
color += inTexture.read(uint2(x3, y3)).xyy;
color += inTexture.read(uint2(x4, y0)).zyy;
color += inTexture.read(uint2(x3, y2)).yxx;
color += inTexture.read(uint2(x1, y3)).yyy;
color += inTexture.read(uint2(x2, y2)).zzx;
color += inTexture.read(uint2(x1, y2)).yyy;
color += inTexture.read(uint2(x3, y0)).zxx;
color += inTexture.read(uint2(x0, y2)).xxz;
color += inTexture.read(uint2(x4, y4)).zzz;
color += inTexture.read(uint2(x0, y2)).xzx;
color += inTexture.read(uint2(x0, y2)).xyx;
color += inTexture.read(uint2(x0, y0)).yzz;
color += inTexture.read(uint2(x4, y0)).xzz;
color += inTexture.read(uint2(x2, y2)).zzz;
color += inTexture.read(uint2(x3, y0)).yxz;
color += inTexture.read(uint2(x0, y3)).yyz;
color += inTexture.read(uint2(x4, y0)).zzz;
color += inTexture.read(uint2(x0, y3)).zxy;
color += inTexture.read(uint2(x3, y1)).yxx;
color += inTexture.read(uint2(x2, y4)).zzx;
color += inTexture.read(uint2(x3, y0)).xxx;
color += inTexture.read(uint2(x0, y2)).zxz;
color += inTexture.read(uint2(x2, y2)).zyy;
color += inTexture.read(uint2(x0, y4)).zzx;
color += inTexture.read(uint2(x1, y4)).yyx;
color += inTexture.read(uint2(x4, y3)).xyy;
color += inTexture.read(uint2(x0, y2)).xyx;
color += inTexture.read(uint2(x0, y2)).xyz;
color += inTexture.read(uint2(x3, y4)).zxz;
color += inTexture.read(uint2(x2, y3)).zxx;
color += inTexture.read(uint2(x0, y2)).yzx;
color += inTexture.read(uint2(x3, y4)).yxy;
color += inTexture.read(uint2(x4, y2)).xxx;
color += inTexture.read(uint2(x0, y1)).yyx;
color += inTexture.read(uint2(x2, y2)).xyx;
color += inTexture.read(uint2(x3, y2)).yyx;
color += inTexture.read(uint2(x2, y3)).zyx;
color += inTexture.read(uint2(x1, y3)).zyy;
color += inTexture.read(uint2(x2, y2)).zyx;
color += inTexture.read(uint2(x3, y0)).yzz;
color += inTexture.read(uint2(x4, y2)).yxz;
color += inTexture.read(uint2(x3, y2)).xzy;
color += inTexture.read(uint2(x3, y1)).zxy;
color += inTexture.read(uint2(x4, y1)).yxy;
color += inTexture.read(uint2(x3, y0)).xzy;
color += inTexture.read(uint2(x1, y3)).zxx;
color += inTexture.read(uint2(x2, y2)).yzz;
color += inTexture.read(uint2(x0, y2)).zyy;
color += inTexture.read(uint2(x4, y3)).zxy;
color += inTexture.read(uint2(x2, y4)).xzx;
color += inTexture.read(uint2(x1, y2)).zzy;
color += inTexture.read(uint2(x1, y1)).yxz;
color += inTexture.read(uint2(x0, y3)).yyx;
color += inTexture.read(uint2(x3, y1)).xyz;
color += inTexture.read(uint2(x0, y1)).yyy;
color += inTexture.read(uint2(x0, y4)).xzz;
color += inTexture.read(uint2(x0, y3)).xyz;
color += inTexture.read(uint2(x4, y0)).xzy;
color += inTexture.read(uint2(x0, y1)).zyy;
color += inTexture.read(uint2(x4, y2)).yxx;
color += inTexture.read(uint2(x1, y3)).xyy;
color += inTexture.read(uint2(x3, y0)).zxy;
color += inTexture.read(uint2(x3, y2)).xxz;
color += inTexture.read(uint2(x1, y1)).yzy;
color += inTexture.read(uint2(x1, y4)).zyx;
color += inTexture.read(uint2(x2, y3)).yyx;
color += inTexture.read(uint2(x1, y3)).yyy;
color += inTexture.read(uint2(x2, y4)).yxy;
color += inTexture.read(uint2(x1, y3)).xxx;
color += inTexture.read(uint2(x0, y3)).yxx;
color += inTexture.read(uint2(x2, y2)).xxx;
color += inTexture.read(uint2(x3, y4)).yzy;
color += inTexture.read(uint2(x2, y1)).xxy;
color += inTexture.read(uint2(x2, y4)).yxy;
color += inTexture.read(uint2(x0, y0)).zzz;
color += inTexture.read(uint2(x1, y0)).yyy;
color += inTexture.read(uint2(x3, y4)).yzx;
color += inTexture.read(uint2(x2, y1)).zyy;
color += inTexture.read(uint2(x2, y0)).zxy;
color += inTexture.read(uint2(x1, y0)).yxx;
color += inTexture.read(uint2(x1, y4)).xxy;
color += inTexture.read(uint2(x4, y4)).xyx;
color += inTexture.read(uint2(x0, y0)).yzx;
color += inTexture.read(uint2(x1, y2)).zxx;
color += inTexture.read(uint2(x2, y4)).yyy;
color += inTexture.read(uint2(x3, y2)).yyz;
color += inTexture.read(uint2(x3, y4)).yxx;
color += inTexture.read(uint2(x2, y3)).zzy;
color += inTexture.read(uint2(x4, y4)).zyx;
color += inTexture.read(uint2(x3, y1)).zzy;
color += inTexture.read(uint2(x0, y4)).xyx;
color += inTexture.read(uint2(x4, y2)).yyx;
color += inTexture.read(uint2(x1, y0)).yxy;
color += inTexture.read(uint2(x2, y2)).xzy;
color += inTexture.read(uint2(x3, y0)).xyx;
color += inTexture.read(uint2(x3, y2)).yyx;
color += inTexture.read(uint2(x1, y1)).zzz;
color += inTexture.read(uint2(x0, y2)).zyz;
color += inTexture.read(uint2(x4, y0)).yxx;
color += inTexture.read(uint2(x2, y1)).xzy;
color += inTexture.read(uint2(x2, y4)).zxz;
color += inTexture.read(uint2(x2, y1)).yyx;
color += inTexture.read(uint2(x2, y4)).yxz;
color += inTexture.read(uint2(x2, y0)).zzx;
color += inTexture.read(uint2(x2, y3)).yyx;
color += inTexture.read(uint2(x4, y3)).zyy;
color += inTexture.read(uint2(x4, y4)).zyx;
color += inTexture.read(uint2(x0, y4)).zyx;
color += inTexture.read(uint2(x1, y0)).zzx;
color += inTexture.read(uint2(x3, y0)).xyz;
color += inTexture.read(uint2(x1, y3)).yxx;
color += inTexture.read(uint2(x2, y2)).yxy;
color += inTexture.read(uint2(x0, y3)).zxy;
color += inTexture.read(uint2(x0, y1)).yxy;
color += inTexture.read(uint2(x3, y1)).xzy;
color += inTexture.read(uint2(x1, y1)).yzz;
color += inTexture.read(uint2(x3, y4)).xzx;
color += inTexture.read(uint2(x0, y3)).yyy;
color += inTexture.read(uint2(x0, y0)).xyx;
color += inTexture.read(uint2(x2, y0)).zyx;
color += inTexture.read(uint2(x4, y3)).xxy;
color += inTexture.read(uint2(x4, y0)).zxy;
color += inTexture.read(uint2(x1, y1)).yyx;
color += inTexture.read(uint2(x0, y1)).zyx;
color += inTexture.read(uint2(x1, y4)).yzx;
color += inTexture.read(uint2(x2, y0)).zzy;
color += inTexture.read(uint2(x0, y2)).xzy;
color += inTexture.read(uint2(x0, y2)).yxx;
color += inTexture.read(uint2(x4, y2)).xxy;
color += inTexture.read(uint2(x3, y2)).yzx;
color += inTexture.read(uint2(x1, y3)).yxx;
color += inTexture.read(uint2(x1, y1)).yyz;
color += inTexture.read(uint2(x3, y2)).xzy;
color += inTexture.read(uint2(x1, y2)).yzy;
color += inTexture.read(uint2(x0, y1)).zzz;
color += inTexture.read(uint2(x3, y1)).zyz;
color += inTexture.read(uint2(x0, y2)).xxz;
color += inTexture.read(uint2(x3, y0)).zyy;
color += inTexture.read(uint2(x0, y1)).xzy;
color += inTexture.read(uint2(x0, y2)).xyz;
color += inTexture.read(uint2(x2, y0)).yyy;
color += inTexture.read(uint2(x0, y1)).xxx;
color += inTexture.read(uint2(x2, y1)).yyy;
color += inTexture.read(uint2(x0, y1)).xxx;
color += inTexture.read(uint2(x4, y4)).zyz;
color += inTexture.read(uint2(x0, y2)).yzy;
color += inTexture.read(uint2(x2, y3)).xzy;
color += inTexture.read(uint2(x3, y4)).yyx;
color += inTexture.read(uint2(x0, y3)).zyz;
color += inTexture.read(uint2(x2, y0)).yyy;
color += inTexture.read(uint2(x2, y2)).yyy;
color += inTexture.read(uint2(x4, y3)).xxz;
color += inTexture.read(uint2(x1, y1)).zyz;
color += inTexture.read(uint2(x1, y0)).yzx;
color += inTexture.read(uint2(x0, y4)).yxx;
color += inTexture.read(uint2(x0, y2)).xyz;
color += inTexture.read(uint2(x2, y4)).zzx;
color += inTexture.read(uint2(x0, y3)).xxy;
color += inTexture.read(uint2(x3, y0)).xzx;
color += inTexture.read(uint2(x3, y3)).xxy;
color += inTexture.read(uint2(x2, y0)).zxy;
color += inTexture.read(uint2(x2, y0)).zzy;
color += inTexture.read(uint2(x0, y1)).zxx;
color += inTexture.read(uint2(x2, y2)).yzx;
color += inTexture.read(uint2(x2, y4)).zyy;
color += inTexture.read(uint2(x4, y2)).xzy;
color += inTexture.read(uint2(x1, y0)).zyy;
color += inTexture.read(uint2(x0, y4)).yxz;
color += inTexture.read(uint2(x4, y4)).yxy;
color += inTexture.read(uint2(x0, y0)).xzy;
color += inTexture.read(uint2(x0, y1)).zyz;
color += inTexture.read(uint2(x1, y1)).zxy;
color += inTexture.read(uint2(x2, y2)).zzy;
color += inTexture.read(uint2(x3, y2)).xyz;
color += inTexture.read(uint2(x3, y2)).zyx;
color += inTexture.read(uint2(x2, y4)).xzx;
color += inTexture.read(uint2(x1, y3)).yyz;
color += inTexture.read(uint2(x3, y4)).yzz;
color += inTexture.read(uint2(x2, y0)).yyx;
color += inTexture.read(uint2(x2, y3)).zzy;
color += inTexture.read(uint2(x3, y3)).yzy;
color += inTexture.read(uint2(x2, y0)).zyz;
color += inTexture.read(uint2(x0, y4)).yzz;
color += inTexture.read(uint2(x1, y3)).xzz;
color += inTexture.read(uint2(x3, y1)).yzy;
color += inTexture.read(uint2(x2, y4)).yzy;
color += inTexture.read(uint2(x2, y2)).zzz;
color += inTexture.read(uint2(x0, y3)).zxx;
color += inTexture.read(uint2(x2, y1)).xyy;
color += inTexture.read(uint2(x3, y1)).xzz;
color += inTexture.read(uint2(x3, y2)).xyx;
color += inTexture.read(uint2(x2, y4)).xxx;
color += inTexture.read(uint2(x0, y0)).xyy;
color += inTexture.read(uint2(x3, y4)).zxy;
color += inTexture.read(uint2(x4, y0)).xzx;
color += inTexture.read(uint2(x2, y2)).zxx;
color += inTexture.read(uint2(x4, y0)).zyx;
color += inTexture.read(uint2(x1, y3)).zxz;
color += inTexture.read(uint2(x4, y1)).yxy;
color += inTexture.read(uint2(x4, y0)).xzx;
color += inTexture.read(uint2(x2, y1)).xyx;
color += inTexture.read(uint2(x3, y1)).xzz;
color += inTexture.read(uint2(x4, y4)).xyz;
color += inTexture.read(uint2(x1, y3)).zxx;
color += inTexture.read(uint2(x2, y4)).xzx;
color += inTexture.read(uint2(x3, y1)).xyz;
color += inTexture.read(uint2(x2, y1)).zyz;
color += inTexture.read(uint2(x3, y0)).yxx;
color += inTexture.read(uint2(x1, y1)).xyy;
color += inTexture.read(uint2(x4, y1)).zzy;
color += inTexture.read(uint2(x3, y1)).xxy;
color += inTexture.read(uint2(x4, y3)).zxy;
color += inTexture.read(uint2(x1, y3)).xzy;
color += inTexture.read(uint2(x3, y3)).zyx;
color += inTexture.read(uint2(x4, y2)).xzx;
color += inTexture.read(uint2(x4, y3)).xzx;
color += inTexture.read(uint2(x1, y3)).xzx;
color += inTexture.read(uint2(x1, y1)).zyz;
color += inTexture.read(uint2(x2, y4)).xxz;
color += inTexture.read(uint2(x3, y4)).xyx;
color += inTexture.read(uint2(x0, y0)).xyz;
color += inTexture.read(uint2(x1, y4)).yyx;
color += inTexture.read(uint2(x2, y3)).zxz;
color += inTexture.read(uint2(x2, y4)).zzy;
color += inTexture.read(uint2(x3, y2)).zzz;
color += inTexture.read(uint2(x0, y3)).yxx;
color += inTexture.read(uint2(x2, y0)).xxx;
color += inTexture.read(uint2(x0, y3)).yzx;
color += inTexture.read(uint2(x3, y0)).xzx;
color += inTexture.read(uint2(x0, y2)).yyx;
color += inTexture.read(uint2(x1, y0)).zzx;
color += inTexture.read(uint2(x0, y0)).xyx;
color += inTexture.read(uint2(x2, y4)).yzz;
color += inTexture.read(uint2(x4, y0)).xyz;
color += inTexture.read(uint2(x1, y0)).zxx;
color += inTexture.read(uint2(x4, y0)).zzx;
color += inTexture.read(uint2(x4, y2)).zyy;
color += inTexture.read(uint2(x1, y1)).zzz;
color += inTexture.read(uint2(x0, y4)).zxz;
color += inTexture.read(uint2(x3, y4)).zyx;
color += inTexture.read(uint2(x4, y1)).zyz;
color += inTexture.read(uint2(x0, y1)).xxz;
color += inTexture.read(uint2(x4, y2)).yxx;
color += inTexture.read(uint2(x4, y3)).zzy;
color += inTexture.read(uint2(x2, y2)).yxx;
color += inTexture.read(uint2(x4, y1)).xyy;
color += inTexture.read(uint2(x0, y1)).xzz;
color += inTexture.read(uint2(x0, y0)).xyz;
color += inTexture.read(uint2(x0, y4)).zyx;
color += inTexture.read(uint2(x1, y3)).yzy;
color += inTexture.read(uint2(x2, y0)).zyy;
color += inTexture.read(uint2(x3, y4)).xzz;
color += inTexture.read(uint2(x0, y3)).xyx;
color += inTexture.read(uint2(x1, y2)).xzy;
color += inTexture.read(uint2(x4, y0)).yzz;
color += inTexture.read(uint2(x0, y0)).yzy;
color += inTexture.read(uint2(x4, y3)).yyx;
color += inTexture.read(uint2(x0, y2)).zzy;
color += inTexture.read(uint2(x2, y4)).xzx;
color += inTexture.read(uint2(x1, y2)).xyx;
color += inTexture.read(uint2(x2, y2)).yxx;
color += inTexture.read(uint2(x4, y1)).yyx;
color += inTexture.read(uint2(x1, y2)).xxx;
color += inTexture.read(uint2(x1, y0)).yzy;
color += inTexture.read(uint2(x2, y3)).zxx;
color += inTexture.read(uint2(x3, y0)).yzz;
color += inTexture.read(uint2(x1, y2)).yyx;
color += inTexture.read(uint2(x3, y2)).yxy;
color += inTexture.read(uint2(x2, y0)).zxx;
color += inTexture.read(uint2(x3, y4)).yyx;
color += inTexture.read(uint2(x0, y0)).zxz;
color += inTexture.read(uint2(x2, y0)).zyx;
color += inTexture.read(uint2(x2, y2)).yxx;
color += inTexture.read(uint2(x2, y2)).yyy;
color += inTexture.read(uint2(x2, y2)).yxx;
color += inTexture.read(uint2(x0, y4)).xzx;
color += inTexture.read(uint2(x3, y0)).yzy;
color += inTexture.read(uint2(x0, y2)).yzz;
color += inTexture.read(uint2(x4, y4)).xyy;
color += inTexture.read(uint2(x1, y0)).zxy;
color += inTexture.read(uint2(x4, y3)).yzx;
color += inTexture.read(uint2(x0, y2)).xxx;
color += inTexture.read(uint2(x0, y1)).yyy;
color += inTexture.read(uint2(x2, y4)).yzx;
color += inTexture.read(uint2(x2, y0)).yxx;
color += inTexture.read(uint2(x4, y2)).xxx;
color += inTexture.read(uint2(x4, y1)).xzz;
color += inTexture.read(uint2(x2, y3)).yzx;
color += inTexture.read(uint2(x1, y1)).zyx;
color += inTexture.read(uint2(x1, y0)).yxx;
color += inTexture.read(uint2(x1, y4)).zxx;
color += inTexture.read(uint2(x4, y3)).zxz;
color += inTexture.read(uint2(x3, y3)).xzy;
color += inTexture.read(uint2(x4, y2)).xxy;
color += inTexture.read(uint2(x4, y2)).xzy;
color += inTexture.read(uint2(x3, y0)).xzx;
color += inTexture.read(uint2(x2, y2)).zyz;
color += inTexture.read(uint2(x3, y0)).yyz;
color += inTexture.read(uint2(x0, y3)).yzx;
color += inTexture.read(uint2(x1, y0)).zxx;
color += inTexture.read(uint2(x0, y4)).xxy;
color += inTexture.read(uint2(x3, y0)).yzy;
color += inTexture.read(uint2(x1, y3)).zxx;
color += inTexture.read(uint2(x0, y1)).xxz;
color += inTexture.read(uint2(x4, y0)).zxy;
color += inTexture.read(uint2(x0, y3)).zyx;
color += inTexture.read(uint2(x2, y3)).yyx;
color += inTexture.read(uint2(x4, y3)).zxz;
color += inTexture.read(uint2(x3, y2)).yxy;
color += inTexture.read(uint2(x3, y1)).zxx;
color += inTexture.read(uint2(x0, y3)).yzz;
color += inTexture.read(uint2(x3, y4)).xzx;
color += inTexture.read(uint2(x0, y1)).yzz;
color += inTexture.read(uint2(x3, y2)).xyy;
color += inTexture.read(uint2(x1, y0)).zyx;
color += inTexture.read(uint2(x4, y4)).xxx;
color += inTexture.read(uint2(x2, y4)).zyy;
color += inTexture.read(uint2(x3, y1)).xyx;
color += inTexture.read(uint2(x2, y3)).yyx;
color += inTexture.read(uint2(x4, y3)).xxz;
color += inTexture.read(uint2(x1, y4)).zyx;
color += inTexture.read(uint2(x3, y1)).xzz;
color += inTexture.read(uint2(x1, y1)).yyx;
color += inTexture.read(uint2(x1, y4)).zxz;
color += inTexture.read(uint2(x1, y0)).zyy;
color += inTexture.read(uint2(x2, y0)).zzz;
color += inTexture.read(uint2(x1, y2)).zzx;
color += inTexture.read(uint2(x1, y4)).xxz;
color += inTexture.read(uint2(x3, y3)).zxy;
color += inTexture.read(uint2(x0, y4)).zyz;
color += inTexture.read(uint2(x0, y4)).xzy;
color += inTexture.read(uint2(x1, y4)).zxy;
color += inTexture.read(uint2(x1, y3)).zxx;
color += inTexture.read(uint2(x3, y3)).zyy;
color += inTexture.read(uint2(x1, y0)).yyx;
color += inTexture.read(uint2(x4, y2)).xzy;
color += inTexture.read(uint2(x0, y2)).yxx;
color += inTexture.read(uint2(x2, y0)).zzx;
color += inTexture.read(uint2(x4, y4)).xzz;
color += inTexture.read(uint2(x0, y3)).xyy;
color += inTexture.read(uint2(x0, y3)).xxy;
color += inTexture.read(uint2(x0, y4)).zxz;
color += inTexture.read(uint2(x4, y4)).xyy;
color += inTexture.read(uint2(x3, y1)).xxz;
color += inTexture.read(uint2(x2, y4)).zzz;
color += inTexture.read(uint2(x1, y1)).xxx;
color += inTexture.read(uint2(x3, y3)).yyx;
color += inTexture.read(uint2(x2, y3)).yxx;
color += inTexture.read(uint2(x2, y3)).zzy;
color += inTexture.read(uint2(x1, y2)).xxz;
color += inTexture.read(uint2(x2, y4)).yxy;
color += inTexture.read(uint2(x2, y2)).zyy;
color += inTexture.read(uint2(x2, y1)).xzx;
color += inTexture.read(uint2(x1, y2)).zzz;
color += inTexture.read(uint2(x2, y0)).zzz;
color += inTexture.read(uint2(x2, y4)).yzx;
color += inTexture.read(uint2(x2, y4)).yzz;
color += inTexture.read(uint2(x2, y2)).xzx;
color += inTexture.read(uint2(x2, y1)).zyy;
color += inTexture.read(uint2(x0, y0)).zxy;
color += inTexture.read(uint2(x2, y4)).xyx;
color += inTexture.read(uint2(x1, y2)).yyx;
color += inTexture.read(uint2(x3, y3)).zyz;
color += inTexture.read(uint2(x0, y0)).yyy;
color += inTexture.read(uint2(x1, y4)).xzz;
color += inTexture.read(uint2(x4, y3)).zxx;
color += inTexture.read(uint2(x4, y0)).zzy;
color += inTexture.read(uint2(x4, y0)).xzx;
color += inTexture.read(uint2(x3, y1)).yxz;
color += inTexture.read(uint2(x3, y1)).yzz;
color += inTexture.read(uint2(x4, y0)).zyy;
color += inTexture.read(uint2(x2, y2)).xzx;
color += inTexture.read(uint2(x0, y2)).zzy;
color += inTexture.read(uint2(x0, y3)).xyy;
color += inTexture.read(uint2(x2, y3)).zyz;
color += inTexture.read(uint2(x3, y3)).yzy;
color += inTexture.read(uint2(x4, y3)).zxz;
color += inTexture.read(uint2(x4, y2)).yyy;
color += inTexture.read(uint2(x3, y1)).zxy;
color += inTexture.read(uint2(x4, y4)).zzx;
color += inTexture.read(uint2(x0, y4)).zxy;
color += inTexture.read(uint2(x4, y2)).zzy;
color += inTexture.read(uint2(x0, y2)).zyz;
color += inTexture.read(uint2(x4, y3)).zyz;
color += inTexture.read(uint2(x1, y1)).xxx;
color += inTexture.read(uint2(x2, y2)).yzz;
color += inTexture.read(uint2(x0, y4)).yzz;
color += inTexture.read(uint2(x1, y2)).zzx;
color += inTexture.read(uint2(x4, y3)).zzy;
color += inTexture.read(uint2(x1, y4)).yzx;
color += inTexture.read(uint2(x3, y0)).yxy;
color += inTexture.read(uint2(x2, y3)).yzy;
color += inTexture.read(uint2(x2, y0)).zzx;
color += inTexture.read(uint2(x1, y3)).zzy;
color += inTexture.read(uint2(x1, y2)).yxx;
color += inTexture.read(uint2(x0, y4)).xzy;
color += inTexture.read(uint2(x3, y0)).xyz;
color += inTexture.read(uint2(x2, y0)).zxx;
color += inTexture.read(uint2(x0, y0)).zxy;
color += inTexture.read(uint2(x4, y0)).yyx;
color += inTexture.read(uint2(x2, y1)).zxy;
color += inTexture.read(uint2(x2, y1)).xyz;
color += inTexture.read(uint2(x0, y2)).xxy;
color += inTexture.read(uint2(x3, y0)).zzz;
color += inTexture.read(uint2(x1, y3)).yxx;
color += inTexture.read(uint2(x1, y3)).yyy;
color += inTexture.read(uint2(x1, y2)).yyx;
color += inTexture.read(uint2(x0, y0)).xzy;
color += inTexture.read(uint2(x4, y1)).zxz;
color += inTexture.read(uint2(x4, y3)).zxz;
color += inTexture.read(uint2(x3, y3)).yzz;
color += inTexture.read(uint2(x3, y2)).xzx;
color += inTexture.read(uint2(x3, y3)).yyz;
color += inTexture.read(uint2(x4, y1)).zzz;
color += inTexture.read(uint2(x0, y0)).xxx;
color += inTexture.read(uint2(x4, y0)).xxy;
color += inTexture.read(uint2(x4, y3)).yyz;
color += inTexture.read(uint2(x0, y1)).xxz;
color += inTexture.read(uint2(x2, y1)).xyz;
color += inTexture.read(uint2(x1, y2)).zxy;
color += inTexture.read(uint2(x3, y3)).zyx;
color += inTexture.read(uint2(x4, y3)).xyy;
color += inTexture.read(uint2(x3, y2)).xzy;
color += inTexture.read(uint2(x2, y4)).yzy;
color += inTexture.read(uint2(x3, y2)).yxx;
color += inTexture.read(uint2(x4, y4)).xyz;
color += inTexture.read(uint2(x4, y2)).yzz;
color += inTexture.read(uint2(x2, y4)).zxy;
color += inTexture.read(uint2(x3, y2)).zyy;
color += inTexture.read(uint2(x1, y4)).yzx;
color += inTexture.read(uint2(x3, y1)).xyy;
color += inTexture.read(uint2(x1, y4)).xyz;
color += inTexture.read(uint2(x3, y2)).xxx;
color += inTexture.read(uint2(x0, y2)).yzx;
color += inTexture.read(uint2(x3, y2)).xzz;
color += inTexture.read(uint2(x2, y4)).zxz;
""".strip().split('\n')

mat = np.zeros((9 * 9 * 3, 9 * 9 * 3), dtype=float)
# (243, 243)

def get(x, y, p):
	x = ((x % 9) + 9) % 9
	y = ((y % 9) + 9) % 9
	return (x * 9 + y) * 3 + {'x': 0, 'y': 1, 'z': 2}[p]

for c in code:
	dy = -(int(c[31]) - 2)
	dx = int(c[35]) - 2
	cx = c[39]
	cy = c[40]
	cz = c[41]
	for x in range(0, 9):
		for y in range(0, 9):
			mat[get(x, y, 'x'), get(x - dx, y - dy, cx), ] += 1
			mat[get(x, y, 'y'), get(x - dx, y - dy, cy), ] += 1
			mat[get(x, y, 'z'), get(x - dx, y - dy, cz), ] += 1
for row in mat:
	print(row)
'''
[ 5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.]
[ 8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.]
[13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.]
[ 4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.]
[ 5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4.]
[10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4.]
[11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.]
[10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6.]
[ 9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4.]
[ 7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.]
[10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.]
[ 6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.]
[ 9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.]
[ 1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.]
[ 4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4.]
[ 9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4.]
[ 7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.]
[10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.]
[13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.]
[ 7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.]
[ 6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.]
[10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6.]
[ 4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.]
[ 4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.]
[ 4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.]
[ 4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10.]
[ 9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.]
[ 2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.]
[ 6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.]
[10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.]
[ 0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.]
[ 7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.]
[ 9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.]
[ 8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.]
[ 9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.]
[ 7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.]
[ 8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.]
[ 9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5.]
[ 6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.]
[ 8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.]
[ 7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  5.  5.  5.  6.  7.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.]
[ 2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  4.  4.  8.  6.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.]
[ 3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  5.  5.  7.  7.  3.  8. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2.]
[ 5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  5.  5.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  7. 10.  8.  1.  7.  9.  4.  5.  6.
  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.]
[ 4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  4.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9. 10.  8.  7.  4.  7.  6.  4.  7.  4.
 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.]
[ 7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  5.  5.  7.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10.]
[ 7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.  3.  4.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.
  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.  9.  1.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.
  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4. 10.  8.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.  6.  3.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.
  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.  3.  9.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.
  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.  9.  5.  7.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.  4.  5.  5.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1.
 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.  7.  4.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.
  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.  7.  8.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5. 10.  4.  5.
  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.
  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.  5. 11.  4.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.
  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10. 10.  8.  4.
 10.  8.  3.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.  7.  5.  7.
  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.
  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.  7.  7.  6.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4.
 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.  6.  9.  7.
  9.  5.  7.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.  3.  7.  9.
  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.
  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10. 10.  6.  4.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4.
 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.  9.  8.  5.
  7.  8.  6.  0.  0.  0.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.  7.  3.  5.
 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.  9. 11. 11.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.  5. 11. 10.
 10.  8.  4. 10.  8.  3.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.  2. 10.  3.
  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4. 11.  5. 15.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.  8.  7. 11.
  6.  9.  7.  9.  5.  7.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.  3.  7.  5.
  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4. 11. 10. 10.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2. 13.  7.  6.
  9.  8.  5.  7.  8.  6.  0.  0.  0.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.  5.  6.  7.
  7.  3.  5. 10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.  9.  3. 12.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  4.  5.  5.
  9. 11. 11.  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.  6.  3. 11.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.  4.  7.  7.
  5. 11. 10. 10.  8.  4. 10.  8.  3.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.  4.  8.  6.
  2. 10.  3.  7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.  7.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.  5.  5.  4.
 11.  5. 15.  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4. 10.  6.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.  5.  6.  7.
  8.  7. 11.  6.  9.  7.  9.  5.  7.]
[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.  7.  3.  8.
  3.  7.  5.  3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.  8. 10.  6.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.  8.  2.  4.
 11. 10. 10. 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.  4.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10. 10.  6.  2.
 13.  7.  6.  9.  8.  5.  7.  8.  6.]
[ 3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  5.  5.
  5.  6.  7.  7.  3.  5. 10.  4.  5.  9.  3. 12.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.  9. 10.  4.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  4.  5.  5.  9. 11. 11.  5. 11.  4.  6.  3. 11.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.  4.  5.  6.
 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. 11.  9.  7.
  4.  7.  7.  5. 11. 10. 10.  8.  4.]
[ 6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  4.
  4.  8.  6.  2. 10.  3.  7.  5.  7.  7.  7. 10.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.  6.  7. 10.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  6.  9.
  5.  5.  4. 11.  5. 15.  7.  7.  6. 10.  6.  4.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.  4.  7.  4.
  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  8. 10.  9.
  5.  6.  7.  8.  7. 11.  6.  9.  7.]
[ 4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  5.  5.  7.
  7.  3.  8.  3.  7.  5.  3.  7.  9.  8. 10.  6.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.  8.  7.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  4.  9.
  8.  2.  4. 11. 10. 10. 10.  6.  4.  4.  8.  8.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.  4.  8.  3.
  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8. 10.
 10.  6.  2. 13.  7.  6.  9.  8.  5.]
[10.  4.  5.  3.  4.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  5.  5.  5.  6.  7.  7.  3.  5.  9. 10.  4.  9.  3. 12.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  8.  4.  4.  0.  7.  9.  2.  5. 15.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5. 11.  4.  9.  1.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  4.  5.  5.  9. 11. 11.  4.  5.  6.  6.  3. 11.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7.  8.  6.  7. 10.  8.  1.  7.  9.
 10.  8.  4. 10.  8.  3.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 11.  9.  7.  4.  7.  7.  5. 11. 10.]
[ 7.  5.  7.  6.  3.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  4.  4.  8.  6.  2. 10.  3.  6.  7. 10.  7.  7. 10.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  6.  6.  7.  5.  4.  6.  8.  8.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  7.  6.  3.  9.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  7.  6.  9.  5.  5.  4. 11.  5. 15.  4.  7.  4. 10.  6.  4.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  7. 10.  4. 10.  8.  7.  4.  7.  6.
  6.  9.  7.  9.  5.  7.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  8. 10.  9.  5.  6.  7.  8.  7. 11.]
[ 3.  7.  9.  4.  5.  5.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  5.  5.  7.  7.  3.  8.  3.  7.  5.  8.  7.  8.  8. 10.  6.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  4.  7.  5.  9.  6.  1. 10.  9.  3.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 10.  6.  4.  7.  4.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  4.  9.  8.  2.  4. 11. 10. 10.  4.  8.  3.  4.  8.  8.  0.  0.  0.
  0.  0.  0.  0.  0.  0.  0.  0.  0.  9.  8.  4. 13.  8.  4.  9.  5.  3.
  9.  8.  5.  7.  8.  6.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
  9.  8. 10. 10.  6.  2. 13.  7.  6.]
'''

mat /= len(code)

const = [
	34.01,
	58.83,
	57.726,
	60.162,
	34.01,
	60.89,
	62.206,
	59.312,
	34.01,
	63.328,
	62.97,
	62.592,
	34.01,
	59.616,
	56.748,
	57.018,
	34.01,
	63.448,
	62.144,
	59.942,
	34.01,
	59.294,
	56.5,
	56.262,
	34.01,
	56.992,
	55.134,
	54.712,
	34.01,
	58.776,
	58.55,
	55.268,
	34.01,
	62.102,
	63.294,
	64.81,
	34.01,
	57.446,
	59.01,
	56.574,
	34.01,
	58.718,
	59.928,
	58.292,
	34.01,
	60.072,
	59.508,
	60.914,
	34.01,
	57.948,
	54.538,
	54.27,
	34.01,
	59.496,
	58.018,
	54.868,
	34.01,
	56.11,
	56.284,
	58.23,
	34.01,
	53.614,
	51.836,
	54.016,
	34.01,
	57.512,
	55.182,
	54.416,
	34.01,
	55.144,
	56.52,
	59.55,
	34.01,
	52.722,
	52.568,
	50.42,
	34.01,
	55.524,
	55.796,
	56.034,
	34.01,
	54.752,
	54.758,
	55.564,
	34.01,
	54.824,
	56.42,
	55.944,
	34.01,
	53.486,
	55.722,
	52.85,
	34.01,
	54.074,
	52.38,
	55.884,
	34.01,
	52.29,
	50.39,
	47.584,
	34.01,
	50.45,
	51.694,
	50.442,
	34.01,
	51.54,
	52.34,
	55.244,
	34.01,
	43.204,
	44.668,
	43.558,
	34.01,
	46.584,
	46.85,
	47.628,
	34.01,
	46.822,
	46.208,
	47.286,
	34.01,
	46.418,
	46.772,
	46.944,
	34.01,
	45.786,
	46.854,
	45.322,
	34.01,
	43.518,
	43.836,
	44.854,
	34.01,
	44.226,
	43.148,
	42.18,
	34.01,
	44.192,
	43.506,
	41.21,
	34.01,
	43.17,
	43.008,
	44.632,
	34.01,
	33.356,
	35.692,
	35.36,
	34.01,
	37.01,
	38.258,
	37.848,
	34.01,
	37.322,
	36.962,
	35.21,
	34.01,
	42.966,
	43.968,
	42.78,
	34.01,
	39.914,
	38.01,
	37.956,
	34.01,
	40.59,
	40.49,
	41.182,
	34.01,
	34.376,
	35.552,
	33.306,
	34.01,
	32.912,
	33.084,
	34.376,
	34.01,
	33.232,
	34.094,
	34.64,
	34.01,
	30.378,
	30.54,
	32.712,
	34.01,
	36.564,
	36.046,
	33.074,
	34.01,
	33.736,
	33.838,
	36.35,
	34.01,
	35.67,
	34.892,
	36.04,
	34.01,
	37.022,
	36.984,
	35.984,
	34.01,
	37.022,
	36.384,
	37.066,
	34.01,
	35.51,
	35.852,
	35.916,
	34.01,
	32.308,
	31.382,
	31.968,
	34.01,
	30.776,
	32.55,
	33.134,
	34.01,
	34.046,
	36.01,
	35.812,
	34.01,
	33.246,
	32.846,
	34.038,
	34.01,
	35.638,
	35.918,
	36.54,
	34.01,
	39.526,
	37.942,
	38.924,
	34.01,
	36.85,
	35.348,
	36.616,
	34.01,
	41.588,
	42.608,
	40.312,
	34.01,
	34.12,
	34.518,
	34.748,
	34.01,
	33.84,
	33.494,
	34.338,
	34.01,
	30.966,
	32.548,
	31.798,
	34.01,
	44.652,
	45.188,
	47.53,
	34.01,
	47.268,
	45.81,
	48.986,
	34.01,
	49.218,
	48.02,
	47.092,
	34.01,
	46.148,
	44.744,
	45.818,
	34.01,
	50.2,
	49.81,
	48.574,
	34.01,
	44.778,
	45.224,
	45.116,
	34.01,
	44.568,
	43.856,
	46.386,
	34.01,
	45.63,
	45.61,
	45.186,
	34.01,
	48.958,
	50.86,
	50.526,
	34.01,
	50.626,
	50.004,
	51.126,
	34.01,
	51.026,
	49.298,
	50.144,
	34.01,
	53.058,
	53.048,
	50.668,
	34.01,
	48.976,
	49.48,
	50.014,
	34.01,
	54.53,
	51.056,
	51.992,
	34.01,
	55.73,
	54.01,
	51.102,
	34.01,
	50.078,
	47.868,
	48.632,
	34.01,
	51.714,
	51.55,
	49.202,
	34.01,
	49.916,
	50.724,
	48.774,
]
# len=324
# const = np.array(const).reshape([-1, 4])
'''
[[34.01  58.83  57.726 60.162]
 [34.01  60.89  62.206 59.312]
 [34.01  63.328 62.97  62.592]
 [34.01  59.616 56.748 57.018]
 [34.01  63.448 62.144 59.942]
 [34.01  59.294 56.5   56.262]
 [34.01  56.992 55.134 54.712]
 [34.01  58.776 58.55  55.268]
 [34.01  62.102 63.294 64.81 ]
 [34.01  57.446 59.01  56.574]
 [34.01  58.718 59.928 58.292]
 [34.01  60.072 59.508 60.914]
 [34.01  57.948 54.538 54.27 ]
 [34.01  59.496 58.018 54.868]
 [34.01  56.11  56.284 58.23 ]
 [34.01  53.614 51.836 54.016]
 [34.01  57.512 55.182 54.416]
 [34.01  55.144 56.52  59.55 ]
 [34.01  52.722 52.568 50.42 ]
 [34.01  55.524 55.796 56.034]
 [34.01  54.752 54.758 55.564]
 [34.01  54.824 56.42  55.944]
 [34.01  53.486 55.722 52.85 ]
 [34.01  54.074 52.38  55.884]
 [34.01  52.29  50.39  47.584]
 [34.01  50.45  51.694 50.442]
 [34.01  51.54  52.34  55.244]
 [34.01  43.204 44.668 43.558]
 [34.01  46.584 46.85  47.628]
 [34.01  46.822 46.208 47.286]
 [34.01  46.418 46.772 46.944]
 [34.01  45.786 46.854 45.322]
 [34.01  43.518 43.836 44.854]
 [34.01  44.226 43.148 42.18 ]
 [34.01  44.192 43.506 41.21 ]
 [34.01  43.17  43.008 44.632]
 [34.01  33.356 35.692 35.36 ]
 [34.01  37.01  38.258 37.848]
 [34.01  37.322 36.962 35.21 ]
 [34.01  42.966 43.968 42.78 ]
 [34.01  39.914 38.01  37.956]
 [34.01  40.59  40.49  41.182]
 [34.01  34.376 35.552 33.306]
 [34.01  32.912 33.084 34.376]
 [34.01  33.232 34.094 34.64 ]
 [34.01  30.378 30.54  32.712]
 [34.01  36.564 36.046 33.074]
 [34.01  33.736 33.838 36.35 ]
 [34.01  35.67  34.892 36.04 ]
 [34.01  37.022 36.984 35.984]
 [34.01  37.022 36.384 37.066]
 [34.01  35.51  35.852 35.916]
 [34.01  32.308 31.382 31.968]
 [34.01  30.776 32.55  33.134]
 [34.01  34.046 36.01  35.812]
 [34.01  33.246 32.846 34.038]
 [34.01  35.638 35.918 36.54 ]
 [34.01  39.526 37.942 38.924]
 [34.01  36.85  35.348 36.616]
 [34.01  41.588 42.608 40.312]
 [34.01  34.12  34.518 34.748]
 [34.01  33.84  33.494 34.338]
 [34.01  30.966 32.548 31.798]
 [34.01  44.652 45.188 47.53 ]
 [34.01  47.268 45.81  48.986]
 [34.01  49.218 48.02  47.092]
 [34.01  46.148 44.744 45.818]
 [34.01  50.2   49.81  48.574]
 [34.01  44.778 45.224 45.116]
 [34.01  44.568 43.856 46.386]
 [34.01  45.63  45.61  45.186]
 [34.01  48.958 50.86  50.526]
 [34.01  50.626 50.004 51.126]
 [34.01  51.026 49.298 50.144]
 [34.01  53.058 53.048 50.668]
 [34.01  48.976 49.48  50.014]
 [34.01  54.53  51.056 51.992]
 [34.01  55.73  54.01  51.102]
 [34.01  50.078 47.868 48.632]
 [34.01  51.714 51.55  49.202]
 [34.01  49.916 50.724 48.774]]
'''

# const = np.array(const).reshape([-1, 4])[..., 1:]
'''
[[58.83  57.726 60.162]
 [60.89  62.206 59.312]
 [63.328 62.97  62.592]
 [59.616 56.748 57.018]
 [63.448 62.144 59.942]
 [59.294 56.5   56.262]
 [56.992 55.134 54.712]
 [58.776 58.55  55.268]
 [62.102 63.294 64.81 ]
 [57.446 59.01  56.574]
 [58.718 59.928 58.292]
 [60.072 59.508 60.914]
 [57.948 54.538 54.27 ]
 [59.496 58.018 54.868]
 [56.11  56.284 58.23 ]
 [53.614 51.836 54.016]
 [57.512 55.182 54.416]
 [55.144 56.52  59.55 ]
 [52.722 52.568 50.42 ]
 [55.524 55.796 56.034]
 [54.752 54.758 55.564]
 [54.824 56.42  55.944]
 [53.486 55.722 52.85 ]
 [54.074 52.38  55.884]
 [52.29  50.39  47.584]
 [50.45  51.694 50.442]
 [51.54  52.34  55.244]
 [43.204 44.668 43.558]
 [46.584 46.85  47.628]
 [46.822 46.208 47.286]
 [46.418 46.772 46.944]
 [45.786 46.854 45.322]
 [43.518 43.836 44.854]
 [44.226 43.148 42.18 ]
 [44.192 43.506 41.21 ]
 [43.17  43.008 44.632]
 [33.356 35.692 35.36 ]
 [37.01  38.258 37.848]
 [37.322 36.962 35.21 ]
 [42.966 43.968 42.78 ]
 [39.914 38.01  37.956]
 [40.59  40.49  41.182]
 [34.376 35.552 33.306]
 [32.912 33.084 34.376]
 [33.232 34.094 34.64 ]
 [30.378 30.54  32.712]
 [36.564 36.046 33.074]
 [33.736 33.838 36.35 ]
 [35.67  34.892 36.04 ]
 [37.022 36.984 35.984]
 [37.022 36.384 37.066]
 [35.51  35.852 35.916]
 [32.308 31.382 31.968]
 [30.776 32.55  33.134]
 [34.046 36.01  35.812]
 [33.246 32.846 34.038]
 [35.638 35.918 36.54 ]
 [39.526 37.942 38.924]
 [36.85  35.348 36.616]
 [41.588 42.608 40.312]
 [34.12  34.518 34.748]
 [33.84  33.494 34.338]
 [30.966 32.548 31.798]
 [44.652 45.188 47.53 ]
 [47.268 45.81  48.986]
 [49.218 48.02  47.092]
 [46.148 44.744 45.818]
 [50.2   49.81  48.574]
 [44.778 45.224 45.116]
 [44.568 43.856 46.386]
 [45.63  45.61  45.186]
 [48.958 50.86  50.526]
 [50.626 50.004 51.126]
 [51.026 49.298 50.144]
 [53.058 53.048 50.668]
 [48.976 49.48  50.014]
 [54.53  51.056 51.992]
 [55.73  54.01  51.102]
 [50.078 47.868 48.632]
 [51.714 51.55  49.202]
 [49.916 50.724 48.774]]
'''

# const = np.array(const).reshape([-1, 4])[..., 1:][..., ::-1]
'''
[[60.162 57.726 58.83 ]
 [59.312 62.206 60.89 ]
 [62.592 62.97  63.328]
 [57.018 56.748 59.616]
 [59.942 62.144 63.448]
 [56.262 56.5   59.294]
 [54.712 55.134 56.992]
 [55.268 58.55  58.776]
 [64.81  63.294 62.102]
 [56.574 59.01  57.446]
 [58.292 59.928 58.718]
 [60.914 59.508 60.072]
 [54.27  54.538 57.948]
 [54.868 58.018 59.496]
 [58.23  56.284 56.11 ]
 [54.016 51.836 53.614]
 [54.416 55.182 57.512]
 [59.55  56.52  55.144]
 [50.42  52.568 52.722]
 [56.034 55.796 55.524]
 [55.564 54.758 54.752]
 [55.944 56.42  54.824]
 [52.85  55.722 53.486]
 [55.884 52.38  54.074]
 [47.584 50.39  52.29 ]
 [50.442 51.694 50.45 ]
 [55.244 52.34  51.54 ]
 [43.558 44.668 43.204]
 [47.628 46.85  46.584]
 [47.286 46.208 46.822]
 [46.944 46.772 46.418]
 [45.322 46.854 45.786]
 [44.854 43.836 43.518]
 [42.18  43.148 44.226]
 [41.21  43.506 44.192]
 [44.632 43.008 43.17 ]
 [35.36  35.692 33.356]
 [37.848 38.258 37.01 ]
 [35.21  36.962 37.322]
 [42.78  43.968 42.966]
 [37.956 38.01  39.914]
 [41.182 40.49  40.59 ]
 [33.306 35.552 34.376]
 [34.376 33.084 32.912]
 [34.64  34.094 33.232]
 [32.712 30.54  30.378]
 [33.074 36.046 36.564]
 [36.35  33.838 33.736]
 [36.04  34.892 35.67 ]
 [35.984 36.984 37.022]
 [37.066 36.384 37.022]
 [35.916 35.852 35.51 ]
 [31.968 31.382 32.308]
 [33.134 32.55  30.776]
 [35.812 36.01  34.046]
 [34.038 32.846 33.246]
 [36.54  35.918 35.638]
 [38.924 37.942 39.526]
 [36.616 35.348 36.85 ]
 [40.312 42.608 41.588]
 [34.748 34.518 34.12 ]
 [34.338 33.494 33.84 ]
 [31.798 32.548 30.966]
 [47.53  45.188 44.652]
 [48.986 45.81  47.268]
 [47.092 48.02  49.218]
 [45.818 44.744 46.148]
 [48.574 49.81  50.2  ]
 [45.116 45.224 44.778]
 [46.386 43.856 44.568]
 [45.186 45.61  45.63 ]
 [50.526 50.86  48.958]
 [51.126 50.004 50.626]
 [50.144 49.298 51.026]
 [50.668 53.048 53.058]
 [50.014 49.48  48.976]
 [51.992 51.056 54.53 ]
 [51.102 54.01  55.73 ]
 [48.632 47.868 50.078]
 [49.202 51.55  51.714]
 [48.774 50.724 49.916]]
'''

const = np.array(const).reshape([-1, 4])[..., 1:][..., ::-1].flatten()
'''
[60.162 57.726 58.83  59.312 62.206 60.89  62.592 62.97  63.328 57.018
 56.748 59.616 59.942 62.144 63.448 56.262 56.5   59.294 54.712 55.134
 56.992 55.268 58.55  58.776 64.81  63.294 62.102 56.574 59.01  57.446
 58.292 59.928 58.718 60.914 59.508 60.072 54.27  54.538 57.948 54.868
 58.018 59.496 58.23  56.284 56.11  54.016 51.836 53.614 54.416 55.182
 57.512 59.55  56.52  55.144 50.42  52.568 52.722 56.034 55.796 55.524
 55.564 54.758 54.752 55.944 56.42  54.824 52.85  55.722 53.486 55.884
 52.38  54.074 47.584 50.39  52.29  50.442 51.694 50.45  55.244 52.34
 51.54  43.558 44.668 43.204 47.628 46.85  46.584 47.286 46.208 46.822
 46.944 46.772 46.418 45.322 46.854 45.786 44.854 43.836 43.518 42.18
 43.148 44.226 41.21  43.506 44.192 44.632 43.008 43.17  35.36  35.692
 33.356 37.848 38.258 37.01  35.21  36.962 37.322 42.78  43.968 42.966
 37.956 38.01  39.914 41.182 40.49  40.59  33.306 35.552 34.376 34.376
 33.084 32.912 34.64  34.094 33.232 32.712 30.54  30.378 33.074 36.046
 36.564 36.35  33.838 33.736 36.04  34.892 35.67  35.984 36.984 37.022
 37.066 36.384 37.022 35.916 35.852 35.51  31.968 31.382 32.308 33.134
 32.55  30.776 35.812 36.01  34.046 34.038 32.846 33.246 36.54  35.918
 35.638 38.924 37.942 39.526 36.616 35.348 36.85  40.312 42.608 41.588
 34.748 34.518 34.12  34.338 33.494 33.84  31.798 32.548 30.966 47.53
 45.188 44.652 48.986 45.81  47.268 47.092 48.02  49.218 45.818 44.744
 46.148 48.574 49.81  50.2   45.116 45.224 44.778 46.386 43.856 44.568
 45.186 45.61  45.63  50.526 50.86  48.958 51.126 50.004 50.626 50.144
 49.298 51.026 50.668 53.048 53.058 50.014 49.48  48.976 51.992 51.056
 54.53  51.102 54.01  55.73  48.632 47.868 50.078 49.202 51.55  51.714
 48.774 50.724 49.916]
'''
# len=243

ans = np.linalg.solve(mat, const)
# 解mat X = const的线性方程组
'''
[ 66. 121. 116. 101.  67.  84.  70. 123.  54.  99.  48.  57.  97.  51.
  56.  48. 100.  55.  50.  99. 101.  99.  49.  54.  52.  57. 102.  55.
  57.  55.  56.  52.  48.  55. 101.  55.  54.  55. 100.  53.  48.  56.
  49.  55.  54. 101.  53.  53.  54.  99.  48.  48. 101.  56. 100.  97.
  49.  54.  97. 101.  55.  48.  49.  98.  54.  97.  52.  56.  52.  56.
  56.  50. 125.  12.  75.   9.  70.   7.  14.  78.  64.  10.  15.   1.
   6.  69.  65.  69.  78.  11.  75.  72.   7.  12.   7.   8.   7.  13.
  79.  69.  69.   1.   6.  72.  76.   9.   3.  69.   6.   6.  11.   9.
   8.   5.   4.   1.   7.  69.  64.  72.   5.  68.   6.  64.   4.  73.
   7.  14.   7.   4.  68.  77.  -0.   9.   4.   5.  71.  10.  75.  72.
   2.   9.  71.  79.   3.   4.   6.  72.  76.  66.   2.   6.  75.   1.
   3.   4.  11.  66.   3.  71.  76.  67.   4.   9.  13.   8.  79.   3.
  64.   0.   7.  77.   6.  71.  11.   1.  10.   2.  13.  72.  70.  71.
   6.   9.  11.  74.   4.   2.   1.  66.  79.  11.  71.   1.   1.  76.
   2.  79.  79.  75.   9.  79.   8.  75.  73.  14.   8.  72.  72.  75.
  69.   0.   7.  15.  67.  79.  65.   7.  78.  66.   4.  66.  79.  74.
  66.  70.  69.   5.  79.  10.   8.  74.   9.  10.  78.  71.  65.  72.
  74.  74.   5.  12.   1.]
'''
ans = np.floor(ans + 0.5).astype(int)
'''
[ 66 121 116 101  67  84  70 123  54  99  48  57  97  51  56  48 100  55
  50  99 101  99  49  54  52  57 102  55  57  55  56  52  48  55 101  55
  54  55 100  53  48  56  49  55  54 101  53  53  54  99  48  48 101  56
 100  97  49  54  97 101  55  48  49  98  54  97  52  56  52  56  56  50
 125  12  75   9  70   7  14  78  64  10  15   1   6  69  65  69  78  11
  75  72   7  12   7   8   7  13  79  69  69   1   6  72  76   9   3  69
   6   6  11   9   8   5   4   1   7  69  64  72   5  68   6  64   4  73
   7  14   7   4  68  77   0   9   4   5  71  10  75  72   2   9  71  79
   3   4   6  72  76  66   2   6  75   1   3   4  11  66   3  71  76  67
   4   9  13   8  79   3  64   0   7  77   6  71  11   1  10   2  13  72
  70  71   6   9  11  74   4   2   1  66  79  11  71   1   1  76   2  79
  79  75   9  79   8  75  73  14   8  72  72  75  69   0   7  15  67  79
  65   7  78  66   4  66  79  74  66  70  69   5  79  10   8  74   9  10
  78  71  65  72  74  74   5  12   1]
'''

img = ans.reshape([9, 9, 3])
'''
[[[ 66 121 116]
  [101  67  84]
  [ 70 123  54]
  [ 99  48  57]
  [ 97  51  56]
  [ 48 100  55]
  [ 50  99 101]
  [ 99  49  54]
  [ 52  57 102]]

 [[ 55  57  55]
  [ 56  52  48]
  [ 55 101  55]
  [ 54  55 100]
  [ 53  48  56]
  [ 49  55  54]
  [101  53  53]
  [ 54  99  48]
  [ 48 101  56]]

 [[100  97  49]
  [ 54  97 101]
  [ 55  48  49]
  [ 98  54  97]
  [ 52  56  52]
  [ 56  56  50]
  [125  12  75]
  [  9  70   7]
  [ 14  78  64]]

 [[ 10  15   1]
  [  6  69  65]
  [ 69  78  11]
  [ 75  72   7]
  [ 12   7   8]
  [  7  13  79]
  [ 69  69   1]
  [  6  72  76]
  [  9   3  69]]

 [[  6   6  11]
  [  9   8   5]
  [  4   1   7]
  [ 69  64  72]
  [  5  68   6]
  [ 64   4  73]
  [  7  14   7]
  [  4  68  77]
  [  0   9   4]]

 [[  5  71  10]
  [ 75  72   2]
  [  9  71  79]
  [  3   4   6]
  [ 72  76  66]
  [  2   6  75]
  [  1   3   4]
  [ 11  66   3]
  [ 71  76  67]]

 [[  4   9  13]
  [  8  79   3]
  [ 64   0   7]
  [ 77   6  71]
  [ 11   1  10]
  [  2  13  72]
  [ 70  71   6]
  [  9  11  74]
  [  4   2   1]]

 [[ 66  79  11]
  [ 71   1   1]
  [ 76   2  79]
  [ 79  75   9]
  [ 79   8  75]
  [ 73  14   8]
  [ 72  72  75]
  [ 69   0   7]
  [ 15  67  79]]

 [[ 65   7  78]
  [ 66   4  66]
  [ 79  74  66]
  [ 70  69   5]
  [ 79  10   8]
  [ 74   9  10]
  [ 78  71  65]
  [ 72  74  74]
  [  5  12   1]]]
'''
img = np.concatenate([img, np.ones_like(img[:, :, :1]) * 255], axis=2)
imageio.imwrite('correct_input.png', img)

print(''.join([chr(i) for i in (ans)]))
```

![]({{site.baseurl}}/img/2021-10-31-correct_input.jpg)

ByteCTF{6c09a380d72cec1649f7978407e767d508176e556c00e8da16ae701b6a484882}