#include <iostream>
#include <vector>
#include <set>

using namespace std;


int main() {

    string s;
    cin >> s;
    vector<int> m;
    for(int i=0; i<s.length(); i++){
        int tmp;
        scanf("%d", &tmp);
        m.push_back(tmp);
    }


    // i为子序列长度
    for(int i=1; i<=s.length()-1; i++){
        set<string> se;
        // 生成子序列集合
        for(int j=0; j+i<=s.length(); j++){
            if(!se.count(s.substr(j, i))){
                se.insert(s.substr(j, i));
            }
        }


        int sum = 0;
        // 遍历子序列集合
        for(auto a : se){
            int num = 0;
            int max = INT32_MIN;
            for(int j=0; j+i<=s.length(); j++){
                if(a == s.substr(j, i)){
                    if(m[j+i-1] > max){
                        num++;
                        max = m[j+i-1];
                    }
                }
            }
            sum += num;
        }
        cout << sum << " ";
    }

    cout << "1" ;

    return 0;
}
