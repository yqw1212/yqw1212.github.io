function main(){
    Java.perform(()=>{
        var abc = Java.use("com.example.re11113.jni");
        var result = abc.getkey();
        console.log(result);
    })
}
main();