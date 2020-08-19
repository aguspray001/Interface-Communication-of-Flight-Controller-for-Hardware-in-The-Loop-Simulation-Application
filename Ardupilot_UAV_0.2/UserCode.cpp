#include "GCS_Mavlink.h"
#include "Plane.h"
#include "version.h"


#define bytesize 85

static void setup_uart(AP_HAL::UARTDriver *uart, const char *name);

char buf[85]; //receiver buffer
char user;
unsigned int j;
struct_a receive; //struct receive data from python
bool flag = false;
aktuator act_x; //struct aktuator
mavlink_hil_state_t packet; // struct mavlink


#if HIL_SUPPORT //kondisi jika HIL SUPPORT aktif
static mavlink_hil_state_t last_hil_state;
#endif



#ifdef USERHOOK_INIT
void Plane::userhook_init()
{

    setup_uart(hal.uartE, "uartE"); //inisialisasi UARTE diaktifkan

}
#endif

/* setup UART at 57600 ---------------------------------------- */
static void setup_uart(AP_HAL::UARTDriver *uart, const char *name)
{
    if (uart == NULL)
    {
        // that UART doesn't exist on this platform
        return;
    }
    ///begin(baudrate,Rx,Tx)
    uart->begin(38400); //baudrate, standart untuk UARTE adalah 38400.
}


////////////////////////////////////////////////////////////////////////////////////////////////// SETUP

#ifdef USERHOOK_FASTLOOP
void Plane::userhook_FastLoop()
{
    // put your 100Hz code here

//list program untuk penerimaan data struct dari raspi melalui serial 
 if(hal.uartE->available() > bytesize)
  {
    for (j = 0; j < sizeof(receive); ++j)
    {
      user = hal.uartE->read();

            if (j ==0)
            {
              if(user == '$')
              {
                buf[0]=user;
                if (buf[0] != '$')
                {
                  j=0;
                }
              }
            }

          if (flag == true)
            {
                memcpy(&receive,buf,sizeof(receive));
            } 


            if(j>0)
                {
                   buf[j]=user;

                  if (buf[j] == '$')
                  {
                    j=0;
                  }
                     if(buf[0] == '$' && buf[32] == '\n')
                        {
                          flag = true;
                        }
                }
    }
  }

}
#endif


#ifdef USERHOOK_50HZLOOP
void Plane::userhook_50Hz()
{
//list program untuk bypass data, filter data yang tidak sempurna, dan pengiriman aktuator.
      if (isnan(receive.speed_data) || isnan(receive.pitch_data)|| isnan(receive.roll_data)|| isnan(receive.yaw_data) 
      || isnan(receive.lat_data) || isnan(receive.lng_data) || isnan(receive.alt_data))
    {
      //nothing to do.
    }
    else {
     if (plane.g.hil_mode == 1) {

        Location loc;

        last_hil_state = packet;

        // set gps hil sensor
        
        memset(&loc, 0, sizeof(loc));
        loc.lat = receive.lat_data*1.0e7f;
        loc.lng = receive.lng_data*1.0e7f;
        loc.alt = receive.alt_data*1.0e2f;
        Vector3f vel(receive.v_x*100, receive.v_y*100, receive.v_z*-100);
        vel *= 0.01f;

        // // setup airspeed pressure based on 3D speed, no wind
        plane.airspeed.setHIL(sq(vel.length()) / 2.0f + 2013);
        uint32_t waktu_us = packet.time_usec;
        // const float magnitude_data = receive.mag_data;

        plane.gps.setHIL(0, AP_GPS::GPS_OK_FIX_3D,
                         packet.time_usec/1000,
                         loc, vel, 10, 0);

         //rad/s
        Vector3f gyros;
        gyros.x = receive.q_x;
        gyros.y = receive.p_y;
        gyros.z = receive.r_z;

        // m/s/s
        Vector3f accels;
        accels.x = receive.a_x;// * GRAVITY_MSS*0.001f;
        accels.y = receive.a_y;// * GRAVITY_MSS*0.001f;
        accels.z = receive.a_z;// * GRAVITY_MSS*0.001f;

        plane.ins.set_gyro(0, gyros);
        plane.ins.set_accel(0, accels);

        // plane.barometer.setHIL(receive.alt_data*0.3048);
        plane.airspeed.setHIL(receive.speed_data, 0, 24); //airspeed, pressure, temperature
        plane.barometer.setHIL(0, 0, 24, receive.alt_data*0.3048, 1, packet.time_usec);
        plane.compass.setHIL(0, radians(receive.roll_data), radians(receive.pitch_data), radians(receive.mag_data));
        plane.compass.setHIL(1, radians(receive.roll_data), radians(receive.pitch_data), radians(receive.mag_data));
        // plane.compass.setHIL(0, radians(magnitude_data), waktu_us);

          if (plane.g.hil_err_limit > 0 &&
            (fabsf(radians(receive.roll_data) - plane.ahrs.roll) > ToRad(plane.g.hil_err_limit) ||
             fabsf(radians(receive.pitch_data) - plane.ahrs.pitch) > ToRad(plane.g.hil_err_limit) ||
             wrap_PI(fabsf(radians(receive.mag_data) - plane.ahrs.yaw)) > ToRad(plane.g.hil_err_limit))) {
            plane.ahrs.reset_attitude(radians(receive.roll_data),radians(receive.pitch_data), radians(receive.mag_data));
        }


        float nilai_ail  = (SRV_Channels::get_output_scaled(SRV_Channel::k_aileron) / 4500.0f);
        float nilai_elv  = (SRV_Channels::get_output_scaled(SRV_Channel::k_elevator) / 4500.0f);
        float nilai_thr  = (SRV_Channels::get_output_scaled(SRV_Channel::k_throttle) / 100.0f);
        float nilai_rudd = (SRV_Channels::get_output_scaled(SRV_Channel::k_rudder) / 4500.0f);

        act_x.x_elv = nilai_elv-0.0273;
        act_x.x_ail = nilai_ail-0.0273;
        act_x.x_thr = nilai_thr;
        act_x.x_rud = nilai_rudd-0.03;

        enum FlightMode effective_mode = control_mode; 
         switch(effective_mode) 
         {
            case STABILIZE:
                act_x.x_elv = receive.pitch_data*-0.01f;
                act_x.x_ail = receive.roll_data*-0.01f;
                act_x.x_rud = 0;
                // throttle is passthrough
                break;
            default:
                break;
      }

        if(hal.uartE->available() == 1 )
          {
            user = hal.uartE->read();
            if (user == 's' )
            {
              control_mode = STABILIZE;
            }

            if (user == 'l' )
            {
              control_mode = LOITER;
            }

            if (user == 'a' )
            {
              control_mode = AUTO;
            }
            if (user == 'm' )
            {
              control_mode = MANUAL;
            }
          } 
          hal.uartE->printf("%f %f %f %f %f %f\n",receive.lat_data, receive.lng_data, receive.alt_data,receive.pitch_data, receive.roll_data,receive.yaw_data);
        // hal.uartE->write((uint8_t*)&act_x,sizeof(act_x)); //pengiriman data menggunakan struct
      }
      
    }

}
#endif

#ifdef USERHOOK_MEDIUMLOOP
void Plane::userhook_MediumLoop()
{
  //10Hz code

}
#endif

#ifdef USERHOOK_SLOWLOOP
void Plane::userhook_SlowLoop()
{
    // put your 3.3Hz code here

}
#endif

#ifdef USERHOOK_SUPERSLOWLOOP
void Plane::userhook_SuperSlowLoop()
{
    // put your 1Hz code here
       
}
#endif