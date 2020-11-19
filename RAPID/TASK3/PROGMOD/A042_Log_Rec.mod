MODULE A042_Log_Rec
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A042 Driver
    !
    ! FUNCTION    :  Inclouds all logger functions 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.03.01 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !                - Philippe Fleischmann
    !                - Michael Lyrenmann
    !                - Gonzalo Casas
    !
    ! License     :  You agree that the software source code and documentation
    !                provided by the copyright holder is confidential, 
    !                and you shall take all reasonable precautions to protect
    !                the source code and documentation, and preserve its confidential,
    !                proprietary and trade secret status in perpetuity. 
    ! 
    !                This license is strictly limited to INTERNAL use within one site.
    !
    !***********************************************************************************

    !************************************************
    ! Declaration :     bool
    !************************************************
    !
    CONST bool b_A042_LogActiv:=TRUE;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    TASK PERS num n_A042_LogMsgCountr:=0;
    TASK PERS num n_A042_FileNr:=1;
    CONST num n_A042_LogMaxMsg:=1000000;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    CONST string st_A042_LogDirPathRC:="RemovableDisk1:A042_Log/";
    CONST string st_A042_LogDirPathVC:="Home:/A042_Log/";
    TASK PERS string st_A042_LogDirPath:="RemovableDisk1:A042_Log/";
    CONST string st_A042_LogFileName:="A042_LogReceiver";
    CONST string st_A042_LogFileFormat:=".csv";
    CONST string st_A042_LogProgrammer:="Philipppe Fleischmann";
    !
    CONST string stTab:="\09";

    ! Global System Data
    TASK PERS string st_RFL_SystemDate:="2018-06-28";
    TASK PERS string st_RFL_SystemTime:="15:49:26";

    !************************************************
    ! Declaration :     iodev
    !************************************************
    !
    VAR iodev iodev_A042_LogFile;

    !************************************************
    ! Declaration :     dir
    !************************************************
    !
    VAR dir dir_A042_Dev;

    !************************************************
    ! Declaration :     clock
    !************************************************
    !
    VAR clock ck_A042_LogTimer;

    !************************************************
    ! Discription :     Steps for log integration in code
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.05.18
    !***************** ETH Zürich *******************
    !
    ! 1. Create a log folder, run the procedure manuali PP to Routine 
    !* r_A042_CrateLogFolder;
    !
    ! 2. Integrate Initialzie log function
    !* r_A042_LogInit
    !
    ! 3. Integrate write log
    !* IF b_A042_LogActiv=TRUE r_A042_LogWriteRhinoMsg message_command;
    !
    ! 4. Integrate Close file (when posible) 
    !* IF b_A042_LogActiv=TRUE r_A042_LogFileClose;
    !
    !************************************************

    !************************************************
    ! Function    :     Log initialization 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.03.01
    !***************** ETH Zürich *******************
    !
    PROC r_A042_LogTest()
        !
        ! Initialize logfile
        r_A042_LogProtInit;
        !
        ! Load protocol message
        ! Header
        pro_A042_ActMsgRob.ProtocolHeader.M_Len:=104;
        pro_A042_ActMsgRob.ProtocolHeader.Ver:=1;
        pro_A042_ActMsgRob.ProtocolHeader.TS_Sec:=33;
        pro_A042_ActMsgRob.ProtocolHeader.TS_NSec:=399;
        !
        ! Main data
        pro_A042_ActMsgRob.ProtocolData.S_ID:=300;
        pro_A042_ActMsgRob.ProtocolData.E_Lev:=0;
        pro_A042_ActMsgRob.ProtocolData.F_Lev:=1;
        pro_A042_ActMsgRob.ProtocolData.I_Len:=8;
        pro_A042_ActMsgRob.ProtocolData.Instr:="MoveAbsJ";
        pro_A042_ActMsgRob.ProtocolData.F_Len:=4;
        pro_A042_ActMsgRob.ProtocolData.Feedb:="Done";
        pro_A042_ActMsgRob.ProtocolData.F_ID:=300;
        !
        ! String parameter
        pro_A042_ActMsgRob.ProtocolData.St_Cnt:=5;
        pro_A042_ActMsgRob.ProtocolData.St1_Len:=4;
        pro_A042_ActMsgRob.ProtocolData.St1:="This";
        pro_A042_ActMsgRob.ProtocolData.St2_Len:=2;
        pro_A042_ActMsgRob.ProtocolData.St2:="is";
        pro_A042_ActMsgRob.ProtocolData.St3_Len:=1;
        pro_A042_ActMsgRob.ProtocolData.St3:="a";
        pro_A042_ActMsgRob.ProtocolData.St4_Len:=8;
        pro_A042_ActMsgRob.ProtocolData.St4:="protocol";
        pro_A042_ActMsgRob.ProtocolData.St5_Len:=5;
        pro_A042_ActMsgRob.ProtocolData.St5:="test";
        !
        ! Value parameter
        pro_A042_ActMsgRob.ProtocolData.V_Cnt:=1;
        pro_A042_ActMsgRob.ProtocolData.V1:=99;
        FOR i FROM 1 TO 1 DO


            r_A042_LogPro pro_A042_ActMsgRob;

        ENDFOR

        Close iodev_A042_LogFile;

        Stop;

        RETURN ;
    ERROR
    ENDPROC

    !************************************************
    ! Function    :     Initialize protocol log 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.03.01
    !***************** ETH Zürich *******************
    !
    PROC r_A042_LogProtInit()
        !
        ! Selcet the writ path for the log file 
        IF RobOS()=TRUE THEN
            !
            ! Real controller write to MemoryStick
            st_A042_LogDirPath:=st_A042_LogDirPathRC;
        ELSE
            !
            ! Virtual controller write to Home
            st_A042_LogDirPath:=st_A042_LogDirPathVC;
        ENDIF
        !
        ! Initalize variables
        n_A042_LogMsgCountr:=0;
        !
        ! Opent directory 
        OpenDir dir_A042_Dev,st_A042_LogDirPath;
        !
        ! Check for log file 
        IF IsFile(st_A042_LogDirPath+st_A042_LogFileName+st_A042_LogFileFormat) THEN
            !
            ! Remove the old log file 
            RemoveFile st_A042_LogDirPath+st_A042_LogFileName+st_A042_LogFileFormat;
        ENDIF
        !
        ! Create and open a new log file 
        Open st_A042_LogDirPath+st_A042_LogFileName+st_A042_LogFileFormat,iodev_A042_LogFile\Write;
        !
        ! Write column title for 
        Write iodev_A042_LogFile,"L-Nr;LogTime;LogFormat;"\NoNewLine;
        Write iodev_A042_LogFile,"M_Len;Ver;TS-Sec;TS-NSec;"\NoNewLine;
        Write iodev_A042_LogFile,"S_ID;E_Lev;I_Len;Instr;F_Lev;F_Len;Feedb;F_ID;"\NoNewLine;
        Write iodev_A042_LogFile,"St_Ctr;St1_Len;St1;St2_Len;St2;St3_Len;St3;St4_Len;St4;St5_Len;St5;"\NoNewLine;
        Write iodev_A042_LogFile,"V_Ctr;V1;V2;V3;V4;V5;V6;V7;V8;V9;V10;"\NoNewLine;
        Write iodev_A042_LogFile,"V11;V12;V13;V14;V15;V16;V17;V18;V19;V20;"\NoNewLine;
        Write iodev_A042_LogFile,"V21;V22;V23;V24;V25;V26;V27;V28;V29;V30;";
        !
        ! Reset and start log timer
        ClkReset ck_A042_LogTimer;
        ClkStart ck_A042_LogTimer;
        !
        ! Log message 
        r_A042_EvLogMsg st_A042_LogFileName,"Log inititalizaion, done";
        RETURN ;
    ERROR
        !
        ! Handle error open directory 
        IF ERRNO=ERR_FILEACC THEN
            !
            ! Create the log folder
            MakeDir st_A042_LogDirPath;
            !
            ! Log message 
            r_A042_EvLogMsg st_A042_LogFileName,"Log Directory created";
            !
            ! Retyry to open directory 
            RETRY;
        ENDIF
        Stop;
        Stop;
    ENDPROC

    !************************************************
    ! Function    :     Log protocol
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.05.18
    !***************** ETH Zürich *******************
    !
    PROC r_A042_LogPro(A042_Protocol proMsg)
        !
        ! Increuse log message counter
        Incr n_A042_LogMsgCountr;
        !
        ! Log only until max message is reached 
        IF n_A042_LogMsgCountr<=n_A042_LogMaxMsg THEN
            !
            ! Add counter nuber and time    
            Write iodev_A042_LogFile,NumToStr(n_A042_LogMsgCountr,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(ClkRead(ck_A042_LogTimer\HighRes),3)+";"\NoNewLine;
            !
            ! Add log format    
            Write iodev_A042_LogFile,"protocol"+";"\NoNewLine;
            !
            ! Add protocol header
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolHeader.M_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolHeader.Ver,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolHeader.TS_Sec,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolHeader.TS_NSec,3)+";"\NoNewLine;
            !
            ! Protocol main data
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.S_ID,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.E_Lev,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.I_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.Instr+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.F_Lev,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.F_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.Feedb+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.F_ID,0)+";"\NoNewLine;
            !
            ! Protocol string parameter
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St_Cnt,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St1_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.St1+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St2_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.St2+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St3_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.St3+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St4_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.St4+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.St5_Len,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,proMsg.ProtocolData.St5+";"\NoNewLine;
            !
            ! Protocol value parameter
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V_Cnt,0)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V1,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V2,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V3,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V4,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V5,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V6,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V7,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V8,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V9,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V10,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V11,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V12,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V13,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V14,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V15,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V16,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V17,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V18,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V19,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V20,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V21,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V22,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V23,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V24,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V25,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V26,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V27,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V28,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V29,3)+";"\NoNewLine;
            Write iodev_A042_LogFile,NumToStr(proMsg.ProtocolData.V30,3)+";"\NoNewLine;
            !
            ! Protocol end
            Write iodev_A042_LogFile,";";
        ENDIF


        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE