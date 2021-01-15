MODULE RFL_Job_Ma
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL
    !
    ! FUNCTION    :  Job Routines for RFL Routines 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2017.07.06 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2017
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Start User Interface System Helper
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.07.06
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_SysHelper()
        !
        WaitSyncTask id_RFL_SysHSta,tl_RFL_All;
        !
        ! Temp Msg for Operator
        TPWrite "Master in RFL System Helper";
        !
        ! Placeholder for Master Code 
        ! 
        WaitSyncTask id_RFL_SysHEnd,tl_RFL_All;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE