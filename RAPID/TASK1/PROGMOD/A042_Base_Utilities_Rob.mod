MODULE A042_Base_Utilities_Rob
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
    ! FUNCTION    :  Base Utilities Library  
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.02.20 Draft
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
    ! Function    :     Read and set jointtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_RasJointtarget()
        !
        ! Read and set robot axis
        jp_A042_Act.robax.rax_1:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V1;
        jp_A042_Act.robax.rax_2:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V2;
        jp_A042_Act.robax.rax_3:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V3;
        jp_A042_Act.robax.rax_4:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V4;
        jp_A042_Act.robax.rax_5:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V5;
        jp_A042_Act.robax.rax_6:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V6;
        !
        ! Read and set external axis
        jp_A042_Act.extax.eax_a:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V7;
        jp_A042_Act.extax.eax_b:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V8;
        jp_A042_Act.extax.eax_c:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V9;
        !
        ! Reserve for unused external axis
        !* jp_A042_Act.extax.eax_d:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V10;
        !* jp_A042_Act.extax.eax_e:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V11;
        !* jp_A042_Act.extax.eax_f:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V12;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read and set robtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_RasRobtarget()
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
        ! Read current data from receiver buffer and set external axis
        p_A042_Act.extax.eax_a:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V8;
        p_A042_Act.extax.eax_b:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V9;
        p_A042_Act.extax.eax_c:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V10;
        !
        ! Reserve for unused external axis
        !* jp_A042_Act.extax.eax_d:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V11;
        !* jp_A042_Act.extax.eax_e:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V12;
        !* jp_A042_Act.extax.eax_f:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.V13;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Update tool center point speed
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_RasTCPSpeed(num nTCPSpeed)
        VAR num nSpeed;
        !
        ! Round input
        nSpeed:=Round(nTCPSpeed\Dec:=2);
        !
        ! Set speed data
        v_A042_Act:=v_A042_Default;
        !
        ! Sanity check       
        IF nSpeed>0 THEN
            !
            ! Good set TCP speed
            v_A042_Act.v_tcp:=nSpeed;
        ELSE
            !
            ! Not good inform user
            !
            ! Load strings for user information
            st_A042_Header:="Update Speed";
            st_A042_ActMsg1:="Requested speed is not posible, minimal value is 0.1 mm/s";
            st_A042_ActMsg2:="Submited speed : "+NumToStr(nSpeed,1)+" mm/s";
            st_A042_ActBtn1:="50 mm/s";
            st_A042_ActBtn2:="100 mm/s";
            st_A042_ActBtn3:="Set my Speed";
            !
            ! Show user window 
            st_A042_UIAnswer:=f_A042_UIMsg(st_A042_Header,st_A042_ActMsg1\stMsgL2:=st_A042_ActMsg2,st_A042_ActBtn1\stBtn2:=st_A042_ActBtn2,\stBtn3:=st_A042_ActBtn3,iconWarning);
            !
            ! Handle user answer
            TEST st_A042_UIAnswer
            CASE st_A042_ActBtn1:
                !
                ! Set default value 1
                v_A042_Act.v_tcp:=v50.v_tcp;
            CASE st_A042_ActBtn2:
                ! 
                ! Set default value 2 
                v_A042_Act.v_tcp:=v100.v_tcp;
            CASE st_A042_ActBtn3:
                !
                ! User interface to set my speed
                v_A042_Act.v_tcp:=f_A042_UINumEntry(st_A042_Header,"Please enter your TCP speed.",0.1,1000,iconInfo);
            DEFAULT:
                !
                ! Program error
                r_A042_ProgError;
            ENDTEST
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read and set zone
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_RasZone(num nZone)
        !
        ! Set zone data
        TEST nZone
        CASE -1:
            !
            ! Fine point
            z_A042_Act:=fine;
        CASE 0:
            !
            ! z0
            z_A042_Act:=z0;
        CASE 1:
            !
            ! z1
            z_A042_Act:=z1;
        CASE 5:
            !
            ! z5
            z_A042_Act:=z5;
        CASE 10:
            !
            ! z10
            z_A042_Act:=z10;
        CASE 15:
            !
            ! z15
            z_A042_Act:=z15;
        CASE 20:
            !
            ! z20
            z_A042_Act:=z20;
        CASE 30:
            !
            ! z30
            z_A042_Act:=z30;
        CASE 40:
            !
            ! z40
            z_A042_Act:=z40;
        CASE 50:
            !
            ! z50
            z_A042_Act:=z50;
        CASE 60:
            !
            ! z60
            z_A042_Act:=z60;
        CASE 80:
            !
            ! z80
            z_A042_Act:=z80;
        CASE 100:
            !
            ! z100
            z_A042_Act:=z100;
        CASE 150:
            !
            ! z150
            z_A042_Act:=z150;
        CASE 200:
            !
            ! z200
            z_A042_Act:=z200;
        DEFAULT:
            !
            ! Use fine point as default
            z_A042_Act:=fine;
        ENDTEST
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read actual jointtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_ReadActJointT(\switch FlyBy)
        !
        ! Wait for Robot in position
        IF NOT Present(FlyBy) WaitRob\InPos;
        !
        ! Read current joint position
        jp_A042_Act:=CJointT();
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read actual robtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_ReadActRobT(\switch FlyBy)
        !
        ! Wait for Robot in position
        IF NOT Present(FlyBy) WaitRob\InPos;
        !
        ! Read current joint position
        p_A042_Act:=CRobT(\Tool:=t_A042_Act\WObj:=ob_A042_Act);
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE