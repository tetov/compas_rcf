MODULE A042_Control_Ma
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
    ! FUNCTION    :  Control modul for the project 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2018.06.17 Draft
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
    ! Function    :     Main for Project A042
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_Main()
        !
        ! Configure communication
        %"r_"+st_RFL_CurMaJob+"_A042_Config"%;
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_MainSta,tl_A042_All;
        !
        ! Message for Operator
        TPWrite "A042 Main";
        !
        ! Init Project
        r_A042_InitCell;
        !
        ! Production loop
        WHILE b_A042_Run=TRUE DO
            !
            ! Check for single and cycle job 
            IF b_A042_Com{n_A042_R1_ChaNr} r_A042_CheckMaJob n_A042_R1_ChaNr;
            !
            ! Check for single and cycle job 
            IF b_A042_Com{n_A042_R2_ChaNr} r_A042_CheckMaJob n_A042_R2_ChaNr;
            !
            ! Check for single and cycle job 
            IF b_A042_Com{n_A042_R3_ChaNr} r_A042_CheckMaJob n_A042_R3_ChaNr;
            !
            ! Check for single and cycle job 
            IF b_A042_Com{n_A042_R4_ChaNr} r_A042_CheckMaJob n_A042_R4_ChaNr;
        ENDWHILE
        !
        ! Message for Operator
        TPWrite "A042 End";
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_MainEnd,tl_A042_All;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Cell
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitCell()
        !
        ! Initialize Global Variables
        r_A042_InitGlobalVar;
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_InitSta,tl_A042_All;
        !
        ! Read system data
        r_A042_ReadSysData;
        !
        ! Initialize IP Address
        r_A042_InitIP;
        !
        ! Initialize Ports
        r_A042_InitPorts;
        !
        ! Initialize Variables
        r_A042_InitVar;
        !
        ! Task synchronisation master data done 
        WaitSyncTask id_A042_InitMa,tl_A042_All;
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_InitEnd,tl_A042_All;
        !
        ! Check rrc connection and bring user message 
        IF b_A042_TaskReceiverOn=TRUE AND b_A042_TaskSenderOn=TRUE THEN
            !
            ! User Message
            r_A042_TPMsg " A042-Connected ";
        ELSEIF b_A042_TaskReceiverOn=TRUE AND b_A042_TaskSenderOn=FALSE THEN
            !
            ! User Message
            r_A042_TPMsg " A042 - Only receiver connected";

        ELSEIF b_A042_TaskReceiverOn=FALSE AND b_A042_TaskSenderOn=TRUE THEN
            !
            ! User Message
            r_A042_TPMsg " A042 - Only sender connected";
        ELSE
            !
            ! User Message
            r_A042_TPMsg " A042 - Not connected";
        ENDIF
        RETURN ;
    ERROR
        !
        ! Check error code
        TPWrite ""\Num:=ERRNO;
        TRYNEXT;
    ENDPROC

    !************************************************
    ! Function    :     Initialize global variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.11.21
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitGlobalVar()
        !
        ! Reset task variables 
        b_A042_TaskReceiverOn:=FALSE;
        b_A042_TaskSenderOn:=FALSE;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.11.21
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitVar()
        !
        ! Reset flag cycle job 
        b_A042_CyclicJob{n_A042_R1_ChaNr}:=FALSE;
        b_A042_CyclicJob{n_A042_R2_ChaNr}:=FALSE;
        b_A042_CyclicJob{n_A042_R3_ChaNr}:=FALSE;
        b_A042_CyclicJob{n_A042_R4_ChaNr}:=FALSE;
        !
        ! Reset flag cycle time running
        b_A042_CycleTimeRunnig{n_A042_R1_ChaNr}:=FALSE;
        b_A042_CycleTimeRunnig{n_A042_R2_ChaNr}:=FALSE;
        b_A042_CycleTimeRunnig{n_A042_R3_ChaNr}:=FALSE;
        b_A042_CycleTimeRunnig{n_A042_R4_ChaNr}:=FALSE;
        !
        ! Reset Read pointer 
        n_A042_ReadPtrRecBuf{n_A042_R1_ChaNr}:=1;
        n_A042_ReadPtrRecBuf{n_A042_R2_ChaNr}:=1;
        n_A042_ReadPtrRecBuf{n_A042_R3_ChaNr}:=1;
        n_A042_ReadPtrRecBuf{n_A042_R4_ChaNr}:=1;
        !
        ! Reset Counter Feedback Value
        n_A042_CounterFStr{n_A042_R1_ChaNr}:=0;
        n_A042_CounterFStr{n_A042_R2_ChaNr}:=0;
        n_A042_CounterFStr{n_A042_R3_ChaNr}:=0;
        n_A042_CounterFStr{n_A042_R4_ChaNr}:=0;
        !
        ! Reset Counter Feedback Value
        n_A042_CounterFVal{n_A042_R1_ChaNr}:=0;
        n_A042_CounterFVal{n_A042_R2_ChaNr}:=0;
        n_A042_CounterFVal{n_A042_R3_ChaNr}:=0;
        n_A042_CounterFVal{n_A042_R4_ChaNr}:=0;
        !
        ! Clear actual sending message
        bm_A042_ActSenMsgMa{n_A042_R1_ChaNr}:=bm_A042_Empty;
        bm_A042_ActSenMsgMa{n_A042_R2_ChaNr}:=bm_A042_Empty;
        bm_A042_ActSenMsgMa{n_A042_R3_ChaNr}:=bm_A042_Empty;
        bm_A042_ActSenMsgMa{n_A042_R4_ChaNr}:=bm_A042_Empty;
        !
        ! Placeholder
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize IP Addresse 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.11.21
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitIP()
        !
        ! Check for automatic or manual IP Address
        IF b_A042_AutoIPAddress=TRUE THEN
            !
            ! Automatic IP Address
            !
            ! Check for real or virtual controller 
            IF RobOS()=TRUE THEN
                !
                ! Real controller
                !
                ! Read current IP Address
                st_A042_IP_Address:=GetSysInfo(\LanIp);
            ELSE
                !
                ! Virtual controller
                !
                ! Set virtual IP Addresse 
                st_A042_IP_Address:=st_A042_IP_AddressVC;
            ENDIF
        ELSE
            !
            ! Manual IP Address
            !
            ! Set manual IP Address
            st_A042_IP_Address:=st_A042_IP_AddressMan;
        ENDIF
        !
        ! Writ event log message for RobotStudio Output
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Actual IP Address: "+st_A042_IP_Address;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Ports 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.06.26
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitPorts()
        !
        ! Default ports 
        n_A042_SocketPortRec:=n_A042_DefaultSocketPortRec;
        n_A042_SocketPortSen:=n_A042_DefaultSocketPortSen;
        !
        ! Check for virtual custom ports
        IF RobOS()=FALSE AND b_A042_VirtualCustomPorts=TRUE THEN
            !
            ! Set virtual custom ports
            n_A042_SocketPortRec:=n_A042_ViCustomSocketPortRec;
            n_A042_SocketPortSen:=n_A042_ViCustomSocketPortSen;
        ENDIF
        !
        ! Writ event log message for RobotStudio Output
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Actual receiver ports: ["+NumToStr(n_A042_SocketPortRec{1},0)+"; "+NumToStr(n_A042_SocketPortRec{2},0)+"; "+NumToStr(n_A042_SocketPortRec{3},0)+"; "+NumToStr(n_A042_SocketPortRec{4},0)+"]";
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Actual sender ports: ["+NumToStr(n_A042_SocketPortSen{1},0)+"; "+NumToStr(n_A042_SocketPortSen{2},0)+"; "+NumToStr(n_A042_SocketPortSen{3},0)+"; "+NumToStr(n_A042_SocketPortSen{4},0)+"]";
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read System Data 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.06.26
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_ReadSysData()
        ! 
        ! Serial  number
        st_A042_SerialNr:=GetSysInfo(\SerialNo);
        !
        ! Software version
        st_A042_SoftwareVersion:=GetSysInfo(\SWVersion);
        !
        ! Software version name 
        !* st_A042_RobotWare:=GetSysInfo(\SWVersionName);
        !
        ! Controller ID
        st_A042_ControllerID:=GetSysInfo(\CtrlId);
        !
        ! WAN IP address
        st_A042_WAN_IP:=GetSysInfo(\LanIp);
        !
        ! Controller language 
        st_A042_ControllerLang:=GetSysInfo(\CtrlLang);
        !
        ! Active system 
        st_A042_SystemName:=GetSysInfo(\SystemName);
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Check for master job
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.21
    !***************** ETH Zürich *******************
    !
    PROC r_A042_CheckMaJob(num nChaNr)
        !
        ! Write current channel number for the instructions 
        n_A042_ChaNr:=nChaNr;
        !
        ! Write current channel task name for the instructions 
        TEST n_A042_ChaNr
        CASE 1:
            !
            ! Set actual channel name 
            st_A042_ChaTask:=ch_A042_Channels.Ch_1.T_Name;
        CASE 2:
            !
            ! Set actual channel name 
            st_A042_ChaTask:=ch_A042_Channels.Ch_2.T_Name;
        CASE 3:
            !
            ! Set actual channel name 
            st_A042_ChaTask:=ch_A042_Channels.Ch_3.T_Name;
        CASE 4:
            !
            ! Set actual channel name 
            st_A042_ChaTask:=ch_A042_Channels.Ch_4.T_Name;
        DEFAULT:
        ENDTEST
        !
        ! Check for job in receiver buffer
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.startbit=TRUE THEN
            !
            ! Execute job from receiver buffer
            r_A042_ExeJobFrmRecBuf;
            !
        ENDIF
        !
        ! Check cyclic job 
        IF b_A042_CyclicJob{n_A042_ChaNr}=TRUE THEN
            !
            ! Check cycle time 
            IF f_A042_CyTiExpired()=TRUE THEN
                !
                ! Call cycle job 
                %st_A042_CyclicJob{n_A042_ChaNr}%;
            ENDIF
        ENDIF
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Execute job from reveicer buffer
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.21
    !***************** ETH Zürich *******************
    !
    PROC r_A042_ExeJobFrmRecBuf()
        !
        ! Call instruction 
        %bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.Instr %;
        !
        ! Set job done
        bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.startbit:=FALSE;
        !
        ! Count read pointer
        IF n_A042_ReadPtrRecBuf{n_A042_ChaNr}<DIM(bm_A042_RecBufferMa,2) THEN
            !
            ! Increas write pointer form buffer
            Incr n_A042_ReadPtrRecBuf{n_A042_ChaNr};
        ELSE
            !
            ! Restart with one
            n_A042_ReadPtrRecBuf{n_A042_ChaNr}:=1;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move message to send buffer master
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.07.09
    !***************** ETH Zürich *******************
    !
    PROC r_A042_MovMsgToSenBufMa(num nChaNr)
        !
        ! Count buffer pointer
        IF n_A042_WritePtrSenBufMa{nChaNr}<DIM(bm_A042_SenBufferMa,2) THEN
            !
            ! Increas write pointer form buffer
            Incr n_A042_WritePtrSenBufMa{nChaNr};
        ELSE
            !
            ! Restart with one
            n_A042_WritePtrSenBufMa{nChaNr}:=1;
        ENDIF
        !
        ! Check for bufferline free to write 
        IF NOT bm_A042_SenBufferMa{nChaNr,n_A042_WritePtrSenBufMa{nChaNr}}.startbit=FALSE THEN
            !
            ! Wait for bufferline free to write 
            WaitUntil bm_A042_SenBufferMa{nChaNr,n_A042_WritePtrSenBufMa{nChaNr}}.startbit=FALSE\PollRate:=0.004;
        ENDIF
        !
        ! Write data in buffer
        bm_A042_SenBufferMa{nChaNr,n_A042_WritePtrSenBufMa{nChaNr}}.Data:=bm_A042_ActSenMsgMa{nChaNr}.Data;
        !
        ! Set Startbit
        bm_A042_SenBufferMa{nChaNr,n_A042_WritePtrSenBufMa{nChaNr}}.startbit:=TRUE;
        !
        ! Clear actual sending message
        bm_A042_ActSenMsgMa{nChaNr}:=bm_A042_Empty;
        !
        ! Reset Counter Feedback String and Value
        n_A042_CounterFStr{nChaNr}:=0;
        n_A042_CounterFVal{nChaNr}:=0;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Cycle time expired 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.27
    ! **************** ETH Zürich *******************
    !
    FUNC bool f_A042_CyTiExpired()
        !
        ! Read current cycle time
        n_A042_ActCycleTime{n_A042_ChaNr}:=ClkRead(ck_A042_CycleJob{n_A042_ChaNr});
        !
        ! Check cycle time expired
        IF n_A042_ActCycleTime{n_A042_ChaNr}>n_A042_MinCycleTime{n_A042_ChaNr} THEN
            !
            ! Store last cycle time 
            n_A042_LastCycleTime{n_A042_ChaNr}:=n_A042_ActCycleTime{n_A042_ChaNr};
            !
            ! Reset clock
            ClkReset ck_A042_CycleJob{n_A042_ChaNr};
            ClkStart ck_A042_CycleJob{n_A042_ChaNr};
            !
            ! Cycle time expired
            RETURN TRUE;
        ELSE
            !
            ! Cycle time not expired
            RETURN FALSE;
        ENDIF
    ERROR
        ! Placeholder for Error Code...
    ENDFUNC


    !************************************************
    ! Function    :     ProgError
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_ProgError()
        ! 
        ! User Info
        TPWrite "Program Error";
        !
        ! Stop Program
        Stop;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE