import "frida-il2cpp-bridge";
 
Il2Cpp.perform(() => {
    console.log(Il2Cpp.unityVersion);
 
    const String = Il2Cpp.corlib.class("System.String");
    Il2Cpp.trace(true).classes(String).and().attach();
});