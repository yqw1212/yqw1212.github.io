import "frida-il2cpp-bridge";
 
Il2Cpp.perform(() => {
    console.log(Il2Cpp.unityVersion);
 
    Il2Cpp.dump("dump.cs", "./")
});