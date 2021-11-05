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
print(mat.shape)

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
# for row in mat:
# 	print(row)

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
print(len(const))
# const = np.array(const).reshape([-1, 4])
# const = np.array(const).reshape([-1, 4])[..., 1:]
# const = np.array(const).reshape([-1, 4])[..., 1:][..., ::-1]
const = np.array(const).reshape([-1, 4])[..., 1:][..., ::-1].flatten()
print(const)
print(len(const))

ans = np.linalg.solve(mat, const)
# 解mat X = const的线性方程组
# print(ans)
ans = np.floor(ans + 0.5).astype(int)
print(ans)

img = ans.reshape([9, 9, 3])
# print(img)
img = np.concatenate([img, np.ones_like(img[:, :, :1]) * 255], axis=2)
imageio.imwrite('correct_input.png', img)

print(''.join([chr(i) for i in (ans)]))
