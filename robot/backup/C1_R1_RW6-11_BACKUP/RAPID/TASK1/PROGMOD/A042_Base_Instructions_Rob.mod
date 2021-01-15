MODULE A042_Base_Instructions_Rob
    !***********************************************************************************
    !
    ! ETH Z�rich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Z�rich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A042 Driver
    !
    ! FUNCTION    :  Base Instracion Library  
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.02.20 Draft
    !
    ! Copyright   :  ETH Z�rich (CH) 2018
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
    ! Function    :     MoveAbsJ
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_MoveAbsJ()
        !
        ! Read and set jonttarget
        r_A042_RasJointtarget;
        !
        ! Read and set tcp speed
        r_A042_RasTCPSpeed bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V13;
        !
        ! Read and set zone 
        r_A042_RasZone bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V14;
        !
        ! Move robot
        MoveAbsJ jp_A042_Act,v_A042_Act,z_A042_Act,t_A042_Act;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined 
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     MoveJ
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_MoveJ()
        !
        ! Read and set robtarget
        r_A042_RASRobtarget;
        !
        ! Read and set tcp speed
        r_A042_RasTCPSpeed bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V14;
        !
        ! Read and set zone 
        r_A042_RasZone bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V15;
        !
        ! Deactivate configuration check
        ConfJ\Off;
        !
        ! Move robot
        MoveJ p_A042_Act,v_A042_Act,z_A042_Act,t_A042_Act\WObj:=ob_A042_Act;
        !
        ! Activate configuration check
        ConfJ\On;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined 
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     MoveL
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_MoveL()
        !
        ! Read and set robtarget
        r_A042_RASRobtarget;
        !
        ! Read and set tcp speed
        r_A042_RasTCPSpeed bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V14;
        !
        ! Read and set zone 
        r_A042_RasZone bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V15;
        !
        ! Deactivate configuration check
        ConfL\Off;
        !
        ! Move robot
        MoveL p_A042_Act,v_A042_Act,z_A042_Act,t_A042_Act\WObj:=ob_A042_Act;
        !
        ! Activate configuration check
        ConfL\On;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined 
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move to frame Joint
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.01.15
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_MoveToFrameJ()
        !
        ! Read current joints 
        jp_A042_Act:=CJointT();
        !
        ! Use current external values 
        p_A042_Act.extax:=jp_A042_Act.extax;
        !
        ! Read current data from receiver buffer and set translation 
        p_A042_Act.trans.x:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        p_A042_Act.trans.y:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V2;
        p_A042_Act.trans.z:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V3;
        !
        ! Read current data from receiver buffer and set rotation (Quaternions) 
        p_A042_Act.rot.q1:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V4;
        p_A042_Act.rot.q2:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V5;
        p_A042_Act.rot.q3:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V6;
        p_A042_Act.rot.q4:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V7;
        !
        ! Read and set tcp speed
        r_A042_RasTCPSpeed bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.v14;
        !
        ! Read and set zone 
        r_A042_RasZone bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.v15;
        !
        ! Deactivate configuration check
        ConfJ\Off;
        !
        ! Move robot
        MoveJ p_A042_Act,v_A042_Act,z_A042_Act,t_A042_Act\WObj:=ob_A042_Act;
        !
        ! Activate configuration check
        ConfJ\On;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined 
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move to frame Linear
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.01.15
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_MoveToFrameL()
        !
        ! Read current joints 
        jp_A042_Act:=CJointT();
        !
        ! Use current external values 
        p_A042_Act.extax:=jp_A042_Act.extax;
        !
        ! Read current data from receiver buffer and set translation 
        p_A042_Act.trans.x:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        p_A042_Act.trans.y:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V2;
        p_A042_Act.trans.z:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V3;
        !
        ! Read current data from receiver buffer and set rotation (Quaternions) 
        p_A042_Act.rot.q1:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V4;
        p_A042_Act.rot.q2:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V5;
        p_A042_Act.rot.q3:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V6;
        p_A042_Act.rot.q4:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V7;
        !
        ! Read and set tcp speed
        r_A042_RasTCPSpeed bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.v14;
        !
        ! Read and set zone 
        r_A042_RasZone bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.v15;
        !
        ! Deactivate configuration check
        ConfL\Off;
        !
        ! Move robot
        MoveL p_A042_Act,v_A042_Act,z_A042_Act,t_A042_Act\WObj:=ob_A042_Act;
        !
        ! Activate configuration check
        ConfL\On;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                DEFAULT:
                    !
                    ! Not defined 
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set analog output
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetAo()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,ao_A042_Act;
        !
        ! Set actual output
        SetAO ao_A042_Act,bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set read ananlog input
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_ReadAi()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,ai_A042_Act;
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Read input value and add it to feedback 
        r_A042_FAddValue AInput(ai_A042_Act);
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 10001,10002,10003,10004:
                !
                ! add robot position  
                r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set group output
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetGo()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,go_A042_Act;
        !
        ! Set actual output
        SetGO go_A042_Act,bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set read group input
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_ReadGi()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,gi_A042_Act;
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Read input value and add it to feedback
        r_A042_FAddValue GInput(gi_A042_Act);
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 10001,10002,10003,10004:
                !
                ! add robot position  
                r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set digital output
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetDo()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,do_A042_Act;
        !
        ! Set actual output
        SetDO do_A042_Act,bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Pulse output
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.08.27
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_PulseDo()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,do_A042_Act;
        !
        ! Set actual output
        PulseDO\High\PLength:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1,do_A042_Act;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set read group input
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_ReadDi()
        !
        ! Get actual output 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,di_A042_Act;
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Read input value and add it to feedback
        r_A042_FAddValue DInput(Di_A042_Act);
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 10001,10002,10003,10004:
                !
                ! add robot position  
                r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
            DEFAULT:
                !
                ! Not defined 
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set tool 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetTool()
        VAR tooldata tX:=[TRUE,[[0,0,0],[1,0,0,0]],[0,[0,0,0],[1,0,0,0],0,0,0]];
        !
        ! Get tool 
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,tX;
        !
        ! Set t_A042_Act 
        t_A042_Act:=tX;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                CASE 10001:
                    !
                    ! Tooldata 
                    ! String 1 from Client
                    r_A042_FAddString bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1;
                    !
                    ! String 2 Structure of parameter information 
                    r_A042_FAddString "Feedback -Tool -Robhold -Pos -Orient -Mass";
                    !
                    ! String 3 roboter hold tool yes or no
                    IF t_A042_Act.robhold=TRUE r_A042_FAddString "Yes";
                    IF t_A042_Act.robhold=FALSE r_A042_FAddString "No";
                    !
                    ! Value 1..3 TCP position xyz 
                    r_A042_FAddValue t_A042_Act.tframe.trans.x;
                    r_A042_FAddValue t_A042_Act.tframe.trans.y;
                    r_A042_FAddValue t_A042_Act.tframe.trans.z;
                    !
                    ! Value 4..7 TCP orientation q1..q4 
                    r_A042_FAddValue t_A042_Act.tframe.rot.q1;
                    r_A042_FAddValue t_A042_Act.tframe.rot.q2;
                    r_A042_FAddValue t_A042_Act.tframe.rot.q3;
                    r_A042_FAddValue t_A042_Act.tframe.rot.q4;
                    !
                    ! Value 8 Tool mass  
                    r_A042_FAddValue t_A042_Act.tload.mass;
                DEFAULT:
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set workobject
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetWobj()
        VAR wobjdata obX:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
        !
        ! Get workobject
        GetDataVal bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1,obX;
        !
        ! Set ob_A042_Act 
        ob_A042_Act:=obX;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Instruction done 
            r_A042_FDone;
            !
            ! Check additional feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Cenerate feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                CASE 10001:
                    !
                    ! Wobjdata 
                    ! String 1 from Client
                    r_A042_FAddString bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1;
                    !
                    ! String 2 Structure of parameter information 
                    r_A042_FAddString "Feedback Workobject -Robhold -UFProg -UFMec -UFPos -UFOrient -OFPos -OFOrient";
                    !
                    ! String 3 roboter hold workobject yes or no
                    IF ob_A042_Act.robhold=TRUE r_A042_FAddString "Yes";
                    IF ob_A042_Act.robhold=FALSE r_A042_FAddString "No";
                    !
                    ! String 4 roboter user frame used yes or no
                    IF ob_A042_Act.ufprog=TRUE r_A042_FAddString "Yes";
                    IF ob_A042_Act.ufprog=FALSE r_A042_FAddString "No";
                    !
                    ! String 5 user frame mechanic
                    r_A042_FAddString ob_A042_Act.ufmec;
                    !
                    ! Value 1..3 user frame position xyz 
                    r_A042_FAddValue ob_A042_Act.uframe.trans.x;
                    r_A042_FAddValue ob_A042_Act.uframe.trans.y;
                    r_A042_FAddValue ob_A042_Act.uframe.trans.z;
                    !
                    ! Value 4..7 user frame orientation q1..q4 
                    r_A042_FAddValue ob_A042_Act.uframe.rot.q1;
                    r_A042_FAddValue ob_A042_Act.uframe.rot.q2;
                    r_A042_FAddValue ob_A042_Act.uframe.rot.q3;
                    r_A042_FAddValue ob_A042_Act.uframe.rot.q4;
                    !
                    ! Value 8..10 object frame position xyz 
                    r_A042_FAddValue ob_A042_Act.oframe.trans.x;
                    r_A042_FAddValue ob_A042_Act.oframe.trans.y;
                    r_A042_FAddValue ob_A042_Act.oframe.trans.z;
                    !
                    ! Value 11..14 object frame orientation q1..q4 
                    r_A042_FAddValue ob_A042_Act.oframe.rot.q1;
                    r_A042_FAddValue ob_A042_Act.oframe.rot.q2;
                    r_A042_FAddValue ob_A042_Act.oframe.rot.q3;
                    r_A042_FAddValue ob_A042_Act.oframe.rot.q4;
                DEFAULT:
                    !
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Get robtarget  
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_GetRobT()
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Get robtarget
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1=1 THEN
            !
            ! Fly by
            r_A042_FActRobT\FlyBy;
        ELSE
            !
            ! In positinton 
            r_A042_FActRobT;
        ENDIF
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Get jointtarget  
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_GetJointT()
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Get robtarget
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1=1 THEN
            !
            ! Fly by
            r_A042_FActJointT\FlyBy;
        ELSE
            !
            ! In positinton 
            r_A042_FActJointT;
        ENDIF
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Start Stopwatch 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_WatchStart()
        !
        ! Reset and start watch
        ClkReset ck_A042_StopWatch;
        ClkStart ck_A042_StopWatch;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Add standard feedback instruction done
            r_A042_FDone;
            !
            ! Feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Check additional feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                CASE 10001,10002,10003,10004:
                    !
                    ! add robot position  
                    r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
                DEFAULT:
                    !
                    ! Not defined 
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Stop Stopwatch
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_WatchStop()
        !
        ! Stop watch and read time 
        ClkStop ck_A042_StopWatch;
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Read stop wacht time and add it to feedback 
        bm_A042_ActSenMsgRob.Data.V1:=ClkRead(ck_A042_StopWatch);
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Add standard feedback instruction done
            r_A042_FDone;
            !
            ! Feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Check additional feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                CASE 10001,10002,10003,10004:
                    !
                    ! add robot position  
                    r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
                DEFAULT:
                    !
                    ! Not defined 
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read Stopwatch
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_WatchRead()
        !
        ! Read stop wacht time and add it to feedback 
        r_A042_FAddValue ClkRead(ck_A042_StopWatch);
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Add standard feedback instruction done
            r_A042_FDone;
            !
            ! Feedback
            IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>1 THEN
                !
                ! Check additional feedback
                TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
                CASE 10001,10002,10003,10004:
                    !
                    ! add robot position  
                    r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
                DEFAULT:
                    !
                    ! Not defined 
                    ! Feedback not supported  
                    r_A042_FError;
                ENDTEST
            ENDIF
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Stop
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.08.27
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_Stop()
        !
        ! Stop task
        Stop;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Wait time
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.08.27
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_WaitTime()
        !
        ! Read time 
        n_A042_Time:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Wait time 
        WaitTime n_A042_Time;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set velocity
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.10.14
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetVel()
        !
        ! Read overide
        n_A042_Override:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Read max TCP
        n_A042_MaxTCP:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V2;
        !
        ! Set max TCP velocity
        VelSet n_A042_Override,n_A042_MaxTCP;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Set acceleration
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.10.14
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_SetAcc()
        !
        ! Read acceleration
        n_A042_Acc:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        !
        ! Read acceleration ramp
        n_A042_Ramp:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V2;
        !
        ! Acceleration set 
        AccSet n_A042_Acc,n_A042_Ramp;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Teachpendant Write
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.10.14
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_TPWrite()
        !
        ! Read Text 
        st_A042_TPWrite:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1;
        !
        ! Clear panel 
        TPErase;
        !
        ! Show message to user 
        TPWrite st_A042_TPWrite;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Dummy
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.08.07
    !***************** ETH Z�rich *******************
    !
    PROC r_A042_Dummy()
        !
        ! Just a dummy procedure for communication tests
        !
        ! Read the current Sequnce ID
        n_A042_Act_S_ID:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.S_ID;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE