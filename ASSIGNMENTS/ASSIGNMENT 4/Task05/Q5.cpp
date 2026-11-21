#include <iomanip>
#include <iostream>
#include <string>
using namespace std;
class Cart {
    string items[10]; double prices[10]; int n=0; double discount=0;
public:
    Cart& add(const string& item,double price){
        if(n<10 && price>=0){items[n]=item;prices[n]=price;++n;}
        return *this;
    }
    Cart& setDiscount(double discount){
        this->discount=discount;
        if(this->discount<0) this->discount=0;
        if(this->discount>100) this->discount=100;
        return *this;
    }
    double total() const {double t=0;for(int i=0;i<n;++i)t+=prices[i];return t*(100-discount)/100;}
    const string& item(int i) const {return items[i];}
};
int main(){
    Cart c;
    c.add("Rice",60).add("Dal",120).setDiscount(10);
    Cart* p=&c; p->add("Oil",180);
    cout<<fixed<<setprecision(2)<<p->total()<<'\n';

    Cart second; second.add("Milk",50).add("Bread",40);
    Cart* carts[]={&c,&second};
    Cart* highest=carts[0];
    for(Cart** it=carts;it<carts+2;++it)
        if((*it)->total()>highest->total()) highest=*it;
    cout<<"Highest cart total: "<<highest->total()<<'\n';
}
