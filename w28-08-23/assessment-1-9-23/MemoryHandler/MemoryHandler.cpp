#include "MemoryHandler.hpp"
std::vector <unsigned char> memReader::getMemberDataFromIndex(size_t index){
    std::vector<unsigned char> bytes;
    size_t offset =0;
    for(size_t x=0; addrOffsetsForObject[x]!= addrOffsetsForObject[index]; x++){
        offset +=addrOffsetsForObject[x];
    }
    unsigned char * pointer = rootAddressForObj+offset;
    for (unsigned char byteOffsets = 0; byteOffsets <addrOffsetsForObject[index]; byteOffsets+=sizeof(unsigned char)){
        bytes.push_back(*(pointer+byteOffsets));
    }

    return bytes;
}
void * memReader::getMemberAddresFromIndex(size_t index){
    size_t offset =0;
    for(size_t x=0; addrOffsetsForObject[x]!= addrOffsetsForObject[index]; x++){
        offset +=addrOffsetsForObject[x];
    }
    unsigned char * pointer = rootAddressForObj+offset;
    return pointer;
}
unsigned char memReader::getClassByteLength(){
    size_t offset =0;
    for(size_t x=0;x != addrOffsetsForObject.size(); x++){
        offset +=addrOffsetsForObject[x];
    }
    return offset;
}
void memReader::_AllocNewMemberArray(size_t byteLength, size_t memberLength){
    //shoot, im not sure how POD/Class types would work with this ... OH well UB is welcome :)
    //creates a new list of things...
    unsigned char byteAlloc =  (byteLength * memberLength);
    //bytelength = size for each index in array
    //member length = size of the array...
    unsigned char arrayStartAddressOffset = getClassByteLength();
    //realloc some memory for struct here...
    //
    // printf("before realloc");

    addrOffsetsForObject.push_back(byteAlloc);

    if (std::realloc(this->rootAddressForObj, (arrayStartAddressOffset+byteAlloc))){

        for(int x =0; x< memberLength; x++){
            //do while x / sizeof(unsigned char) ?? So unhinnged lol
            // std::cout<<x<<" is x\n";
            int xtemp = byteLength;
            do {
                // std::cout<<xtemp<<" is x temp\n";
                rootAddressForObj[(xtemp+arrayStartAddressOffset)+(x*byteLength)] = (unsigned char)(0);
            }while((xtemp-=(sizeof(unsigned char))) != 0);
        }
    }
    else  {
        throw std::bad_alloc(); 
    
    };
    //array address start + it's length = new length... Init to zero?? Maybe implement some sort of hashmap that is used to init objects/primitives...



}