MODULE RFL_Helper_Sen
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIP CO 11.1 / Gustave-Naville-Weg 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL
    !
    ! FUNCTION    :  Helper Routines for ETH
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2018.11.20 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     TP Message User Information
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.19
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_TPMsg(string stMsg)
        ! 
        ! Clear Msg Panel
        TPErase;
        !
        ! Msg for user
        TPWrite stMsg;
        !
        ! Time to read the Msg
        WaitTime n_RFL_TimeTPMsg;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Log Message User Information
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.04.26
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_LogMsg(string stHeader,string stMsg)
        ! 
        ! Msg for user
        ErrWrite \I, stHeader+" "+stMsg,"rLogMsg";
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
ENDMODULE