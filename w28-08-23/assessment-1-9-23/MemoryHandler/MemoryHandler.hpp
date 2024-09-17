#pragma once
#include <iostream>
#include <vector>
#include <cstdint>

struct memReader{
    //this code is unhinged ...
    //BUT I CANNOT STOP 

    unsigned char * rootAddressForObj = nullptr;
    //this knows how to offset because it iterates through 0 -> target index, counts the offsets of the last ones
    //than it reads member using offsets
    //....very unhinged and slow lmao, getting a member is big O(n) where n is length of members lmaooo
    std::vector<unsigned char> addrOffsetsForObject;
    //address offsets for members, kinda bad variable name but it does work with more complex structs too. Hopefully can work recursively too.

    // memReader * handleType(){};
    std::vector <unsigned char> getMemberDataFromIndex(size_t index);
    unsigned char getClassByteLength();
    void * getMemberAddresFromIndex(size_t index);
    void _AllocNewMemberArray(size_t byteLength, size_t memberLength);


};
template<typename ...Args>
memReader * _Struct(Args...args){
    memReader * ptr = new memReader();
    int64_t size = 0;
    int dummy []= {(ptr->addrOffsetsForObject.push_back(sizeof(args)), size += sizeof(args),0)...};
    ptr->rootAddressForObj = (unsigned char*) malloc(size );
    unsigned char * iterPtr= ptr->rootAddressForObj;
    int dummy2 [] = {(*(Args*)iterPtr = args,iterPtr+=sizeof(args),0)...};
    return ptr;

};
