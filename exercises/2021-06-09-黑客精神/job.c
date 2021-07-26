#include <stdio.h>

int main(){
    char result[13] = {'E','o','P','A','o','Y','6','2','@','E','l','R','D'};
    char key[17] = {'W','3','_','a','r','E','_','w','h','O',
                    '_','w','e','_','A','R','E'};
    int v9 = 2016, v11;
    for(int i=0; i<13; i++){
        if ( i % 3 == 1 ){
          v9 = (v9 + 5) % 16;
          v11 = key[v9 + 1];
        }
        else if ( i % 3 == 2 ){
          v9 = (v9 + 7) % 15;
          v11 = key[v9 + 2];
        }
        else{
          v9 = (v9 + 3) % 13;
          v11 = key[v9 + 3];
        }
        printf("%c", v11^result[i]);
    }
    return 0;
}
