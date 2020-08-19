typedef struct
{
  char header[4];
  float waktu; 
  float speed_data;
  float gnd_speed;
  int16_t a_x;
  int16_t a_y;
  int16_t a_z;
  float q_x;
  float p_y;
  float r_z;
  float pitch_data;
  float roll_data;
  float yaw_data;
  float mag_data;
  float lat_data;
  float lng_data;
  float alt_data;
  float x_pos;
  float y_pos;
  float v_x;
  float v_y;
  float v_z;
  char footer;
  
} struct_a;


 typedef struct
 {
   char header[4] = {'$','\0','\0','\0'};
   float x_elv;
   float x_ail;
   float x_rud;
   float x_thr;
   char footer[4] = {'\0','\0','\0','\n'};
 } aktuator;

//273 //273 //300 /0