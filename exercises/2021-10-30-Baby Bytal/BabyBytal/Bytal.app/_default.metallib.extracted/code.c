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