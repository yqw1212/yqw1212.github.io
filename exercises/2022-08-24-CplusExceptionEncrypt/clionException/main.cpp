#include <iostream>

using namespace std;

int main(){
    try{
        int a;
        cin >> a;
        if (a == 0){
            throw("a==0");
        }
    }catch (const char* msg){
        std::cout << msg << " error";
    }
}