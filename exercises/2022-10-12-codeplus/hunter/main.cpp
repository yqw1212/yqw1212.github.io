#include <iostream>
#include <vector>
#include <queue>
#include <set>


using namespace std;


int success = 0;
int x = INT32_MAX;
int y = 0;

void beat(int city, set<int> book, vector<vector<int>> road, vector<int> blood, queue<int> nai, vector<int> tool, vector<int> get, int k){
    // 打怪

    // 不使用道具
    queue<int> naicopy(nai);
    while(!naicopy.empty()){
        // 当前武器可以打败
        if(naicopy.front() >= blood[city]){
            naicopy.front() -= blood[city];
            blood[city] = 0;
            break;
        }else {
            // 当前武器不可以打败, 换武器
            blood[city] -= naicopy.front();
            naicopy.pop();
        }
    }

    // 打败
    if(blood[city]==0){
        // 结束
        if(book.size()==road.size()){
            success = 1;
            if(k-naicopy.size() < x){
                x = k-naicopy.size();
                y = naicopy.front();
            }else if(k-naicopy.size() == x){
                if(y < naicopy.front()){
                    y = naicopy.front();
                }
            }
            return;
        }

        // 该城市是否有道具
        if(tool[city]!=0){
            get.push_back(city);
        }

        // 去下一城市
        for(int i=0; i<road.size(); i++){
            // 该城市未去过 且 有路
            if(!book.count(i) && road[city][i]==1){
                book.insert(i);

                beat(i, book, road, blood, naicopy, tool, get, k);

                book.erase(i);
            }
        }
    }else{ // 未打败
        // 使用道具
        // 尝试每一个道具
        for(int i=0; i<get.size(); i++){
            blood[city] -= get[i];

            // 打
            queue<int> naicopy2(nai);
            while(!naicopy2.empty()){
                // 当前武器可以打败
                if(naicopy2.front() >= blood[city]){
                    naicopy2.front() -= blood[city];
                    blood[city] = 0;
                    break;
                }else {
                    // 当前武器不可以打败, 换武器
                    blood[city] -= naicopy2.front();
                    naicopy2.pop();
                }
            }

            // 成功
            if(blood[city]==0){
                // 结束
                if(book.size()==road.size()){
                    success = 1;
                    if(k-naicopy.size() < x){
                        x = k-naicopy.size();
                        y = naicopy.front();
                    }else if(k-naicopy.size() == x){
                        if(y < naicopy.front()){
                            y = naicopy.front();
                        }
                    }
                    return;
                }

                // 该城市是否有道具
                if(tool[city]!=0){
                    get.push_back(city);
                }

                // 去下一城市
                for(int j=0; j<road.size(); j++){
                    // 该城市未去过 且 有路
                    if(!book.count(j) && road[city][j]==1){
                        book.insert(j);

                        beat(j, book, road, blood, naicopy2, tool, get, k);

                        book.erase(j);
                    }
                }
            }else{
                // 失败
            }

            blood[city] += get[i];
        }
    }
}


int main() {
    // 城市 道路 武器 道具
    int n, m, k, q;
    scanf("%d %d %d %d", &n, &m, &k, &q);

    vector<vector<int>> road(n, vector<int>(n, 0));
    for(int i=0; i<m; i++){
        int from, to;
        scanf("%d %d", &from, &to);
        road[from-1][to-1] = 1;
        road[to-1][from-1] = 1;
    }

    vector<int> blood;
    for(int i=0; i<n; i++){
        int tmp;
        scanf("%d", &tmp);
        blood.push_back(tmp);
    }

    queue<int> nai;
    for(int i=0; i<k; i++){
        int tmp;
        scanf("%d", &tmp);
        nai.push(tmp);
    }

    vector<int> tool(n, 0);
    for(int i=0; i<q; i++){
        int city, d;
        scanf("%d %d", &city, &d);
        tool[city-1] = d;
    }

    // 得到的道具,存放城市编号
    vector<int> get;

    // 从第i个城市出发
    // 这时肯定没有道具
    for(int i=0; i<n; i++) {
        set<int> book;
        book.insert(i);
        beat(i, book, road, blood, nai, tool, get, k);
    }

    if(success==1) {
        cout << x << " " << y;
    }else{
        cout << "FAIL" ;
    }

    return 0;
}
