MODULE A042_Base_Feedback_Rob
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
    ! FUNCTION    :  Base Feedback Library  
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
    ! Function    :     Feedback add string 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.26
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FAddString(string stString)
        !
        ! Increase feedback string counter 
        Incr n_A042_CounterFStr;
        !
        ! Select string to add
        TEST n_A042_CounterFStr
        CASE 1:
            !
            ! Add string
            bm_A042_ActSenMsgRob.Data.St1:=stString;
        CASE 2:
            !
            ! Add string
            bm_A042_ActSenMsgRob.Data.St2:=stString;
        CASE 3:
            !
            ! Add string
            bm_A042_ActSenMsgRob.Data.St3:=stString;
        CASE 4:
            !
            ! Add string
            bm_A042_ActSenMsgRob.Data.St4:=stString;
        CASE 5:
            !
            ! Add string
            bm_A042_ActSenMsgRob.Data.St5:=stString;
        DEFAULT:
            !
            ! Program error
            r_A042_ProgError;
        ENDTEST
        !
        ! Update string counter
        bm_A042_ActSenMsgRob.Data.St_Cnt:=n_A042_CounterFStr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback add value
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.26
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FAddValue(num nValue)
        !
        ! Increase feedback value counter 
        Incr n_A042_CounterFVal;
        !
        ! Select value to add
        TEST n_A042_CounterFVal
        CASE 1:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V1:=nValue;
        CASE 2:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V2:=nValue;
        CASE 3:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V3:=nValue;
        CASE 4:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V4:=nValue;
        CASE 5:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V5:=nValue;
        CASE 6:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V6:=nValue;
        CASE 7:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V7:=nValue;
        CASE 8:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V8:=nValue;
        CASE 9:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V9:=nValue;
        CASE 10:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V10:=nValue;
        CASE 11:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V11:=nValue;
        CASE 12:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V12:=nValue;
        CASE 13:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V13:=nValue;
        CASE 14:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V14:=nValue;
        CASE 15:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V15:=nValue;
        CASE 16:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V16:=nValue;
        CASE 17:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V17:=nValue;
        CASE 18:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V18:=nValue;
        CASE 19:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V19:=nValue;
        CASE 20:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V20:=nValue;
        CASE 21:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V21:=nValue;
        CASE 22:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V22:=nValue;
        CASE 23:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V23:=nValue;
        CASE 24:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V24:=nValue;
        CASE 25:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V25:=nValue;
        CASE 26:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V26:=nValue;
        CASE 27:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V27:=nValue;
        CASE 28:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V28:=nValue;
        CASE 29:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V29:=nValue;
        CASE 30:
            !
            ! Add value
            bm_A042_ActSenMsgRob.Data.V30:=nValue;
        DEFAULT:
            !
            ! Program error
            r_A042_ProgError;
        ENDTEST
        !
        ! Update value counter
        bm_A042_ActSenMsgRob.Data.V_Cnt:=n_A042_CounterFVal;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback done
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FDone()
        !
        ! Add Sqz_ID from Client in Feedback ID
        bm_A042_ActSenMsgRob.Data.F_ID:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.S_ID;
        !
        ! Instruction 
        bm_A042_ActSenMsgRob.Data.Instr:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.Instr;
        !
        ! Feedback 
        bm_A042_ActSenMsgRob.Data.Feedb:="Done";
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback Position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FPos(num nFL)
        !
        ! Check feedback level
        TEST nFL
        CASE 10001:
            !
            ! add robot position after robot is in position  
            r_A042_FActRobT;
        CASE 10002:
            !
            ! add fly by robot positon 
            r_A042_FActRobT\FlyBy;
        CASE 10003:
            !
            ! add robot joints after robot is in position  
            r_A042_FActJointT;
        CASE 10004:
            !
            ! add fly by joints positon 
            r_A042_FActJointT\FlyBy;
        ENDTEST
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback actual jointtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FActJointT(\switch FlyBy)
        !
        ! Read actual jointtartet
        r_A042_ReadActJointT\FlyBy?FlyBy;
        !
        ! Read robot axis
        r_A042_FAddValue jp_A042_Act.robax.rax_1;
        r_A042_FAddValue jp_A042_Act.robax.rax_2;
        r_A042_FAddValue jp_A042_Act.robax.rax_3;
        r_A042_FAddValue jp_A042_Act.robax.rax_4;
        r_A042_FAddValue jp_A042_Act.robax.rax_5;
        r_A042_FAddValue jp_A042_Act.robax.rax_6;
        !
        ! Read external axis
        r_A042_FAddValue jp_A042_Act.extax.eax_a;
        r_A042_FAddValue jp_A042_Act.extax.eax_b;
        r_A042_FAddValue jp_A042_Act.extax.eax_c;
        !
        ! Reserve for unused external axis
        r_A042_FAddValue jp_A042_Act.extax.eax_d;
        r_A042_FAddValue jp_A042_Act.extax.eax_e;
        r_A042_FAddValue jp_A042_Act.extax.eax_f;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback actual robtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FActRobT(\switch FlyBy)
        !
        ! Read actual robtarget
        r_A042_ReadActRobT\FlyBy?FlyBy;
        !
        ! Read actual translation 
        r_A042_FAddValue p_A042_Act.trans.x;
        r_A042_FAddValue p_A042_Act.trans.y;
        r_A042_FAddValue p_A042_Act.trans.z;
        !
        ! Read actual rotation (Quaternions) 
        r_A042_FAddValue p_A042_Act.rot.q1;
        r_A042_FAddValue p_A042_Act.rot.q2;
        r_A042_FAddValue p_A042_Act.rot.q3;
        r_A042_FAddValue p_A042_Act.rot.q4;
        !
        ! Read actual external axis
        r_A042_FAddValue p_A042_Act.extax.eax_a;
        r_A042_FAddValue p_A042_Act.extax.eax_b;
        r_A042_FAddValue p_A042_Act.extax.eax_c;
        !
        ! Reserve for unused external axis
        r_A042_FAddValue p_A042_Act.extax.eax_d;
        r_A042_FAddValue p_A042_Act.extax.eax_e;
        r_A042_FAddValue p_A042_Act.extax.eax_f;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Feedback error 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_FError()
        !
        ! Feedback error with feedback code
        bm_A042_ActSenMsgRob.Data.Feedb:="Done FError "+NumToStr(bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev,0);
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE