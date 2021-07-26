
Java.perform(function(){
    Java.use("ba").b.implementation = function (input, key, iv)
    {
        var result = this.b(input, key, iv);
        console.log("args0: "+input+" args1: "+key+" args2: "+iv+" result: "+result);
        return result;
    }
});