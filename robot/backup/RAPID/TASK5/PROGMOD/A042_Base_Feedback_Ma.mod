MODULE A042_Base_Feedback_Ma
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
    ! HISTORY     :  2020.02.21 Draft
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
        Incr n_A042_CounterFStr{n_A042_ChaNr};
        !
        ! Select string to add
        TEST n_A042_CounterFStr{n_A042_ChaNr}
        CASE 1:
            !
            ! Add string
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St1:=stString;
        CASE 2:
            !
            ! Add string
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St2:=stString;
        CASE 3:
            !
            ! Add string
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St3:=stString;
        CASE 4:
            !
            ! Add string
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St4:=stString;
        CASE 5:
            !
            ! Add string
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St5:=stString;
        DEFAULT:
            !
            ! Program error
            r_A042_ProgError;
        ENDTEST
        !
        ! Update string counter
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.St_Cnt:=n_A042_CounterFStr{n_A042_ChaNr};
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
        Incr n_A042_CounterFVal{n_A042_ChaNr};
        !
        ! Select value to add
        TEST n_A042_CounterFVal{n_A042_ChaNr}
        CASE 1:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V1:=nValue;
        CASE 2:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V2:=nValue;
        CASE 3:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V3:=nValue;
        CASE 4:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V4:=nValue;
        CASE 5:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V5:=nValue;
        CASE 6:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V6:=nValue;
        CASE 7:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V7:=nValue;
        CASE 8:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V8:=nValue;
        CASE 9:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V9:=nValue;
        CASE 10:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V10:=nValue;
        CASE 11:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V11:=nValue;
        CASE 12:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V12:=nValue;
        CASE 13:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V13:=nValue;
        CASE 14:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V14:=nValue;
        CASE 15:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V15:=nValue;
        CASE 16:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V16:=nValue;
        CASE 17:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V17:=nValue;
        CASE 18:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V18:=nValue;
        CASE 19:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V19:=nValue;
        CASE 20:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V20:=nValue;
        CASE 21:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V21:=nValue;
        CASE 22:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V22:=nValue;
        CASE 23:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V23:=nValue;
        CASE 24:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V24:=nValue;
        CASE 25:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V25:=nValue;
        CASE 26:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V26:=nValue;
        CASE 27:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V27:=nValue;
        CASE 28:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V28:=nValue;
        CASE 29:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V29:=nValue;
        CASE 30:
            !
            ! Add value
            bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V30:=nValue;
        DEFAULT:
            !
            ! Program error
            r_A042_ProgError;
        ENDTEST
        !
        ! Update value counter
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.V_Cnt:=n_A042_CounterFVal{n_A042_ChaNr};
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
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.F_ID:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.S_ID;
        !
        ! Instruction 
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.Instr:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.Instr;
        !
        ! Feedback 
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.Feedb:="Master Done";
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Cycle Feedback done
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.04.17
    !***************** ETH Zürich *******************
    !
    PROC r_A042_CyFDone()
        !
        ! Add cyclic jop Sqz_ID from cyclic job start instruction 
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.F_ID:=n_A042_CyJobStart_S_ID{n_A042_ChaNr};
        !
        ! Add cyclic jop instruction
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.Instr:=st_A042_CyclicJob{n_A042_ChaNr};
        !
        ! Feedback 
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.Feedb:="Master Done";
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
        bm_A042_ActSenMsgMa{n_A042_ChaNr}.Data.Feedb:="Master Done FError "+NumToStr(bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev,0);
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE