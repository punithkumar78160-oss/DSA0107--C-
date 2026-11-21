#include <iostream>
#include <memory>
#include <string>
#include <vector>
using namespace std;

class Vehicle {
protected:
    string registration;
    double dailyRate;
    bool rented=false;
public:
    Vehicle(string reg,double rate):registration(move(reg)),dailyRate(rate){}
    virtual double rentalCharge(int days) const=0;
    virtual string type() const=0;
    virtual void rent(){if(rented) throw runtime_error("already rented");rented=true;}
    virtual double returnVehicle(int lateDays) {
        if(!rented) throw runtime_error("vehicle was not rented");
        rented=false;
        return rentalCharge(0)+lateDays*dailyRate*1.5;
    }
    virtual void list() const {
        cout<<type()<<" "<<registration<<" daily=Rs "<<dailyRate
            <<" status="<<(rented?"Rented":"Available")<<'\n';
    }
    virtual ~Vehicle()=default;
};
class Bicycle:public Vehicle {
public:
    Bicycle(string r,double rate):Vehicle(move(r),rate){}
    double rentalCharge(int days) const override{return dailyRate*days;}
    string type() const override{return "Bicycle";}
};
class MotorVehicle:public Vehicle {
protected:
    double fuelLevel; string serviceDue;
public:
    MotorVehicle(string r,double rate,double fuel,string due)
        :Vehicle(move(r),rate),fuelLevel(fuel),serviceDue(move(due)){}
};
class TwoWheeler:public MotorVehicle {
public:
    TwoWheeler(string r,double rate,double fuel,string due):MotorVehicle(move(r),rate,fuel,move(due)){}
    double rentalCharge(int days) const override{return dailyRate*days+50;}
    string type() const override{return "TwoWheeler";}
};
class Car:public MotorVehicle {
protected:int seats;
public:
    Car(string r,double rate,double fuel,string due,int s):MotorVehicle(move(r),rate,fuel,move(due)),seats(s){}
    double rentalCharge(int days) const override{return dailyRate*days+100;}
    string type() const override{return "Car";}
};
class ElectricCar:public Car {
    double batteryKwh;
public:
    ElectricCar(string r,double rate,double battery,string due,int s)
        :Car(move(r),rate,0,move(due),s),batteryKwh(battery){}
    double rentalCharge(int days) const override{return dailyRate*days+batteryKwh*2.0;}
    string type() const override{return "ElectricCar";}
};
class ElectricBus:public Vehicle {
    int seats; double batteryKwh;
public:
    ElectricBus(string r,double rate,int s,double b):Vehicle(move(r),rate),seats(s),batteryKwh(b){}
    double rentalCharge(int days) const override{return dailyRate*days+batteryKwh*2.0+200;}
    string type() const override{return "ElectricBus";}
};

int main(){
    vector<unique_ptr<Vehicle>> fleet;
    fleet.push_back(make_unique<Bicycle>("B-101",100));
    fleet.push_back(make_unique<TwoWheeler>("T-202",250,5,"2026-12-01"));
    fleet.push_back(make_unique<Car>("C-303",1200,30,"2026-12-15",5));
    fleet.push_back(make_unique<ElectricCar>("E-404",1500,60,"2026-12-20",5));
    fleet.push_back(make_unique<ElectricBus>("EB-505",3000,40,180)); // new type added without editing existing classes

    for(auto& v:fleet){v->rent();v->list();cout<<"Charge for 2 days: Rs "<<v->rentalCharge(2)<<'\n';}
    cout<<"Late return charge (2 late days) for first vehicle: Rs "
        <<fleet[0]->returnVehicle(2)<<'\n';
    for(auto& v:fleet) if(v->type()!="Bicycle") v->returnVehicle(1);
    for(const auto& v:fleet) v->list();
}
