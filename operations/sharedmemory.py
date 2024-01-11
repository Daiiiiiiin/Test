import  sys
import  os
import  time
import  threading
import  json
import  serial
import  spidev
import  RPi.GPIO    as      GPIO

import  numpy       as      np
from    collections import  deque
import matplotlib.pyplot as plt

# sys.stdout.reconfigure(encoding='utf-8')

# ANSI escape sequences
UP = lambda x : f"\033[{x}A"
CLR = "\033[0K"
NRM = "\033[0m"

# Colors
RED = "\033[31m"
ORG = "\033[33m"
GRN = "\033[32m"
YEL = "\033[33m"
BLU = "\033[34m"
MAG = "\033[35m"
CYN = "\033[36m"
GRY = "\033[90m"

# Text styles
BLD = "\033[1m"
ITL = "\033[3m"
UND = "\033[4m"

# Two-line (double) box drawing characters
TLLRBAR = "\u2550" # ═
TLUDBAR = "\u2551" # ║
TLULCOR = "\u2552" # ╒
TLURCOR = "\u2555" # ╕
TLLLCOR = "\u2558" # ╘
TLLRCOR = "\u255B" # ╛
TLCRBAR = "\u2560" # ╠
TLCLBAR = "\u2563" # ╣
TLCUBAR = "\u2566" # ╦
TLCDBAR = "\u2569" # ╩
TLCABAR = "\u256C" # ╬

# Single-line (light) box drawing characters
LRBAR = "\u2500" # ─
UDBAR = "\u2503" # │
ULCOR = "\u250F" # ┏
URCOR = "\u2513" # ┓
LLCOR = "\u2517" # ┗
LRCOR = "\u251B" # ┛
CRBAR = "\u251C" # ├
CLBAR = "\u2524" # ┤

CIRCL = "\u25CF"


class SharedMemory:

    def __init__(self, params, prof_t, prof_O2, prof_CH4, log_O2, log_CH4):

        with open(params) as json_file: params = json.load(json_file)

        """ Serial Params """
        serial_port             = params["SERIAL_PORT"          ]
        serial_baudrate         = params["SERIAL_BAUDRATE"      ]
        serial_timeout          = params["SERIAL_TIMEOUT"       ]

        self.serial_api = serial.Serial(
            port        = serial_port,
            baudrate    = serial_baudrate,
            timeout     = serial_timeout
        )

        self.temp = 0

        """ GPIO Params """

        ### GPIO Pin ###
        self.pin_Act_1          = params["PIN_ACT_1"            ]
        self.pin_Act_2          = params["PIN_ACT_2"            ]
        self.pin_SV_bent        = params["PIN_SV_BENT"          ]
        self.pin_SV_OF          = params["PIN_SV_OF"            ]
        self.pin_SV_FC          = params["PIN_SV_FC"            ]
        self.pin_Spark          = params["PIN_SPARK"            ]
        self.pin_Spark_en       = params["PIN_SPARK_EN"         ]
        self.pin_MT_O2_dir      = params["PIN_MT_O2_DIR"        ]
        self.pin_MT_O2_step     = params["PIN_MT_O2_STEP"       ]
        self.pin_MT_CH4_dir     = params["PIN_MT_CH4_DIR"       ]
        self.pin_MT_CH4_step    = params["PIN_MT_CH4_STEP"      ]
        self.pin_Enable         = params["PIN_ENABLE"           ]
        
        ### GPIO Pin initial condition ###
        self.pin_Act_1_0        = params["PIN_ACT_1_0"          ]
        self.pin_Act_2_0        = params["PIN_ACT_2_0"          ]
        self.pin_SV_bent_0      = params["PIN_SV_BENT_0"        ]    
        self.pin_SV_OF_0        = params["PIN_SV_OF_0"          ]
        self.pin_SV_FC_0        = params["PIN_SV_FC_0"          ]
        self.pin_Spark_0        = params["PIN_SPARK_0"          ]
        self.pin_Spark_en_0     = params["PIN_SPARK_EN_0"       ]    
        self.pin_MT_O2_dir_0    = params["PIN_MT_O2_DIR_0"      ]    
        self.pin_MT_O2_step_0   = params["PIN_MT_O2_STEP_0"     ]    
        self.pin_MT_CH4_dir_0   = params["PIN_MT_CH4_DIR_0"     ]    
        self.pin_MT_CH4_step_0  = params["PIN_MT_CH4_STEP_0"    ]
        self.pin_Enable_0       = params["PIN_ENABLE_0"         ]

        """ Operation params """

        ## Motor control
        self.Gear               = params["MT_GEAR"              ]
        self.SPR                = params["MT_SPR"               ]
        self.RPM                = params["MT_RPM"               ]
        self.MT_delay           = params["MT_DELAY"             ]
        self.MT_O2_ang_bias     = params["MT_O2_ANG_BIAS"       ]
        self.MT_O2_ang_init     = params["MT_O2_ANG_INIT"       ]
        self.MT_CH4_ang_init    = params["MT_CH4_ANG_INIT"      ]
        self.MT_CH4_ang_bias    = params["MT_CH4_ANG_BIAS"      ]

        ## Spark Plug
        self.spark_durationTime = params["SPARK_DURATION"       ]
        self.spark_On           = params["SPARK_ON"             ]
        self.spark_Off          = params["SPARK_OFF"            ]

        ## Measure params
        self.measure_chan_O2    = params["MEASURE_O2_CHANNEL"   ]
        self.measure_factor_O2  = params["MEASURE_O2_FACTOR"    ]
        self.measure_bias_O2    = params["MEASURE_O2_BIAS"      ]
        self.measure_chan_CH4   = params["MEASURE_CH4_CHANNEL"  ]
        self.measure_factor_CH4 = params["MEASURE_CH4_FACTOR"   ]
        self.measure_bias_CH4   = params["MEASURE_CH4_BIAS"     ]
        self.filter_windowsize  = params["WINDOW_SIZE"          ]

        """ Controller params """

        ## PI gain
        self.Kp_O2              = params["CONTROL_O2_KP"        ]
        self.Ki_O2              = params["CONTROL_O2_KI"        ]
        self.Kw_O2              = params["CONTROL_O2_KW"        ]
        self.Kp_CH4             = params["CONTROL_CH4_KP"       ]
        self.Ki_CH4             = params["CONTROL_CH4_KI"       ]
        self.Kw_CH4             = params["CONTROL_CH4_KW"       ]

        # FFI2 gain
        self.gain1              = params["CONTROL_FFI2_GAIN1"   ]
        self.gain2              = params["CONTROL_FFI2_GAIN2"   ]

        ## actuator model gain
        self.Ka                 = params["ACTUATOR_GAIN"        ]
        
        ## angle rate & angle limits
        self.min_angrate        = params["ACTUATOR_MIN_ANGRATE" ]
        self.max_angrate        = params["ACTUATOR_MAX_ANGRATE" ]
        self.min_ang            = params["ACTUATOR_MIN_ANG"     ]
        self.max_ang            = params["ACTUATOR_MAX_ANG"     ]
        self.angvel             = params["ACTUATOR_ANGVEL"      ]
        
        ## tank pressure predictor gain
        self.alp                = params["P_TANK_PREDICTOR_GAIN"]

        ## rates
        self.measure_loop_dt    = params["MEASURE_LOOP_DT"       ]
        self.control_loop_dt    = params["CONTROL_LOOP_DT"       ]
        self.logging_loop_dt    = params["LOGGING_LOOP_DT"       ]


        """ INITIALIZING VARIABLES """

        ## Init motor params
        self.REV                = 1*self.Gear
        self.StepDelay          = 1/(self.RPM/60*self.SPR)/2
        self.Turn               = int(self.REV*self.SPR)
        self.OneTickAng         = 360/self.Gear/self.SPR 
        self.HalfTickAng        = self.OneTickAng/2 

        ## SPI set
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1350000

        """ GPIO PIN SETUP """

        GPIO.setwarnings(False)

        ### GPIO Mode setup ###
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_Act_1,                          GPIO.OUT)
        GPIO.setup(self.pin_Act_2,                          GPIO.OUT)
        GPIO.setup(self.pin_SV_bent,                        GPIO.OUT)
        GPIO.setup(self.pin_SV_OF,                          GPIO.OUT)
        GPIO.setup(self.pin_SV_FC,                          GPIO.OUT)
        GPIO.setup(self.pin_MT_O2_dir,                      GPIO.OUT)
        GPIO.setup(self.pin_MT_O2_step,                     GPIO.OUT)
        GPIO.setup(self.pin_MT_CH4_dir,                     GPIO.OUT)
        GPIO.setup(self.pin_MT_CH4_step,                    GPIO.OUT)
        GPIO.setup(self.pin_Enable,                         GPIO.OUT)
        GPIO.setup(self.pin_Spark,                          GPIO.OUT)
        GPIO.setup(self.pin_Spark_en,                       GPIO.OUT)
        GPIO.setup(12,                                      GPIO.OUT)

        ## GPIO initial condition
        GPIO.output(self.pin_Act_1,           self.pin_Act_1_0      )
        GPIO.output(self.pin_Act_2,           self.pin_Act_2_0      )
        GPIO.output(self.pin_SV_bent,         self.pin_SV_bent_0    )
        GPIO.output(self.pin_SV_OF,           self.pin_SV_OF_0      )
        GPIO.output(self.pin_SV_FC,           self.pin_SV_FC_0      )
        GPIO.output(self.pin_Spark,           self.pin_Spark_0      )
        GPIO.output(self.pin_Spark_en,        self.pin_Spark_en_0   )
        GPIO.output(self.pin_MT_O2_dir,       self.pin_MT_O2_dir_0  )
        GPIO.output(self.pin_MT_O2_step,      self.pin_MT_O2_step_0 )
        GPIO.output(self.pin_MT_CH4_dir,      self.pin_MT_CH4_dir_0 )
        GPIO.output(self.pin_MT_CH4_step,     self.pin_MT_CH4_step_0)
        GPIO.output(self.pin_Enable,          self.pin_Enable_0     )
        GPIO.output(12,                                     True    )

        """ Presure data """

        ## Ppc command profile
        self.prof_t             = prof_t
        self.prof_O2            = prof_O2  
        self.prof_CH4           = prof_CH4  

        ## Ppc logs
        self.log_PpcO2          = log_O2
        self.log_PpcCH4         = log_CH4

        ## measurements
        self.Ppc_raw            = {"O2" : 0,      "CH4" : 0 }       # raw data
        self.Ppc_flt            = {"O2" : 0,      "CH4" : 0 }       # filtered
        
        ## commands
        self.Ppc_cmd            = {"O2" : 0,      "CH4" : 0 }       # commands
        self.Ppc_prf            = {"O2" : 0,      "CH4" : 0 }       # profiles
        self.Ppc_tprf           = 0                                # timespace
        
        ## residuals
        self.Ppc_errprev        = {"O2" : 0,      "CH4" : 0 }       # residual prev
        self.Ppc_errcurr        = {"O2" : 0,      "CH4" : 0 }       # residual curr
        self.Ppc_errcum         = {"O2" : 0,      "CH4" : 0 }       # cumulative

        ## tank pressure predictions
        self.Pt_pred            = {"O2" : 0,      "CH4" : 0 }       # predictive Pt

        """ Valve angle data"""

        ## cumulatives
        self.bvang              = {"O2" : 0,      "CH4" : 0 }       # cumulative angle
        self.bvang_measured     = {"O2" : 0,      "CH4" : 0 }       # measured by STM

        ## commands
        self.bvang_cmd          = {"O2" : 0,      "CH4" : 0 }       # angle command
        self.bvstep_in          = {"O2" : 0,      "CH4" : 0 }       # step input command

        """ Time data """
        
        ## runtime
        self.runtime            = -1                                # time from mission start to current

        ## schedule
        self.schedule           = 0                                 # time schedule

        """ Log data """
        
        self.logdata            = 0

        """ flags """

        self.is_running         = False
        self.is_setup_done      = False
