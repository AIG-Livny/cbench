#include <inttypes.h>
#include <time.h>
#include <stdio.h>
#include "cvector.h"
#include "cvector_utils.h"

// Delete max and min measurements
void remove_min_max(cvector_vector_type(clock_t) times){
    cvector_iterator(clock_t) it;
    if ( cvector_size(times) > 10 ) {
        for(int i = 0 ; i < cvector_size(times)/100; i++){
            clock_t max = times[0];
            int maxpos = 0;
            clock_t min = times[0];
            int minpos = 0;

            cvector_for_each_in(it, times){
                if(*it > max){
                    max = *it;
                    maxpos = it - times;
                }
                if(*it < min){
                    min = *it;
                    minpos = it - times;
                }
            }
            cvector_erase(times,maxpos);
            cvector_erase(times,minpos);
        }
    }
}

double get_median_time(cvector_vector_type(clock_t) times){
    cvector_iterator(clock_t) it;

    remove_min_max(times);

    clock_t max = 0;
    double  average = 0;
    cvector_for_each_in(it, times){
        if(*it > max){
            max = *it;
        }
        average += *it;
    }
    average /= cvector_size(times);

    // median
    double sum = 0;
    cvector_for_each_in(it, times){
        double sub = 1.0 - (((double)*it - average)/(double)max);
        sum += *it * sub * sub * sub;
    }

    return sum / cvector_size(times);
}

double get_average_time(cvector_vector_type(clock_t) times){
    cvector_iterator(clock_t) it;
    remove_min_max(times);
    double  sum = 0;
    cvector_for_each_in(it, times){
        sum += *it;
    }
    return sum/cvector_size(times);
}

double get_fastest_time(cvector_vector_type(clock_t) times){
    cvector_iterator(clock_t) it;

    clock_t max = 0;
    cvector_for_each_in(it, times){
        if(*it > max){
            max = *it;
        }
    }
    return max;
}

#define BENCH_MULTIPLE_TIMEBLOCK_START(name,_times) \
{ \
    cvector(clock_t) times = NULL; \
    cvector_reserve(times,_times); \
    unsigned long _i=0; \
    for(; _i < _times; _i++){ \
        clock_t time_start = clock()


#define BENCH_MULTIPLE_TIMEBLOCK_STOP(name) \
        clock_t time_stop = clock(); \
        cvector_push_back(times, time_stop - time_start); \
    } \
    double avg = get_average_time(times); \
    printf("BENCH "#name" n=%lu t=%.2f\n", _i, avg); \
}


struct s1 {int8_t i;};
struct s2 {struct s1 i[2];};
struct s4 {struct s2 i[2];};
struct s8 {struct s4 i[2];};
struct s16 {struct s8 i[2];};
struct s32 {struct s16 i[2];};
struct s64 {struct s32 i[2];};
struct s128 {struct s64 i[2];};
struct s256 {struct s128 i[2];};
struct s512 {struct s128 i[2];};

char glob = 0;

#define FUNC_IMPL(_s) \
__attribute__((noinline)) struct _s by_value_##_s##_all(const struct _s a1, const struct _s a2){ \
    struct _s tmp; \
    for(unsigned int i = 0; i < sizeof(struct _s); i++){ \
        ((char*)&tmp)[i] = ((char*)&a1)[i] + ((char*)&a2)[i]; \
        glob+=((char*)&tmp)[i]; \
    } \
    return tmp; \
} \
 \
__attribute__((noinline)) void by_pointer_##_s##_all(struct _s* result, const struct _s* a1, const struct _s* a2) { \
    for(unsigned int i = 0; i < sizeof(struct _s); i++){ \
        ((char*)result)[i] = ((char*)a1)[i] + ((char*)a2)[i]; \
        glob+=((char*)result)[i]; \
    } \
} \
 \
__attribute__((noinline)) struct _s by_value_##_s##_one(const struct _s a1, const struct _s a2){ \
    struct _s tmp; \
    ((char*)&tmp)[0] = ((char*)&a1)[0] + ((char*)&a2)[0]; \
    glob+=((char*)&tmp)[0]; \
    return tmp; \
} \
 \
__attribute__((noinline)) void by_pointer_##_s##_one(struct _s* result, const struct _s* a1, const struct _s* a2) { \
    ((char*)result)[0] = ((char*)a1)[0] + ((char*)a2)[0]; \
    glob+=((char*)result)[0]; \
}

// All or one byte process
FUNC_IMPL(s1);
FUNC_IMPL(s2);
FUNC_IMPL(s4);
FUNC_IMPL(s8);
FUNC_IMPL(s16);
FUNC_IMPL(s32);
FUNC_IMPL(s64);
FUNC_IMPL(s128);
FUNC_IMPL(s256);
FUNC_IMPL(s512);


#define BENCH(_s,_n) \
{ \
    struct _s a1; \
    struct _s a2; \
    memset(&a1,1,sizeof(struct _s)); \
    memset(&a2,2,sizeof(struct _s)); \
    BENCH_MULTIPLE_TIMEBLOCK_START(_s by_value,_n); \
    struct _s result = by_value_##_s##_one(a1,a2); \
    glob += *(char*)&result; \
    BENCH_MULTIPLE_TIMEBLOCK_STOP(_s by_value one byte process); \
    \
    BENCH_MULTIPLE_TIMEBLOCK_START(_s by_pointer,_n); \
    struct _s result; \
    by_pointer_##_s##_one(&result,&a1,&a2); \
    glob += *(char*)&result; \
    BENCH_MULTIPLE_TIMEBLOCK_STOP(_s by_pointer one byte process); \
    \
    BENCH_MULTIPLE_TIMEBLOCK_START(_s by_value,_n); \
    struct _s result; \
    by_value_##_s##_all(a1,a2); \
    glob += *(char*)&result; \
    BENCH_MULTIPLE_TIMEBLOCK_STOP(_s by_value all bytes process); \
    \
    BENCH_MULTIPLE_TIMEBLOCK_START(_s by_pointer,_n); \
    struct _s result; \
    by_pointer_##_s##_all(&result,&a1,&a2); \
    glob += *(char*)&result; \
    BENCH_MULTIPLE_TIMEBLOCK_STOP(_s by_pointer all bytes process); \
    printf("\n"); \
}

int main ( int argc, char* argv[] ) {

    BENCH(s1,  100000);
    BENCH(s2,  100000);
    BENCH(s4,  100000);
    BENCH(s8,  100000);
    BENCH(s16, 100000);
    BENCH(s32, 100000);
    BENCH(s64, 100000);
    BENCH(s128,100000);
    BENCH(s256,100000);
    BENCH(s512,100000);
    printf("%d",glob);
    return 0;
}