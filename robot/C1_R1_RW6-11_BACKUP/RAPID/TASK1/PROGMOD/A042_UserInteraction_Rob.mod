MODULE A042_UserInteraction_Rob(NOSTEPIN)
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
    ! FUNCTION    :  General Utilities Library  
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
    ! Function    :     Teach Pendant (old FelxPendant) Message
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.03.12
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_TPMsg(string stMsg)
        ! 
        ! Clear Msg Panel
        TPErase;
        !
        ! Msg for user
        TPWrite stMsg;
        !
        ! Time to read the Msg
        WaitTime n_A042_TimeTPMsg;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Teach Pendant (old FelxPendant) Error Message
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.03.12
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_TPErrMsg(num nErrno\switch StopTask\switch StopAllTasks)
        ! 
        ! Clear Msg Panel
        TPErase;
        !
        ! Write error number
        TPWrite "ERRNO = "\Num:=nErrno;
        !
        ! Stop task
        IF Present(StopTask) Stop;
        !
        ! Stop all normal tasks
        IF Present(StopAllTasks) Stop\AllMoveTasks;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Event Log Message
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.03.12
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_EvLogMsg(string stHeader,string stMsg)
        ! 
        ! Msg for user
        ErrWrite\I,stHeader+" "+stMsg,"rLogMsg";
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     User interface message 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.06
    ! **************** ETH Zürich *******************
    !
    FUNC string f_A042_UIMsg(string stMsgHeader,string stMsgL1,\string stMsgL2,\string stMsgL3,\string stMsgL4,\string stMsgL5,string stBtn1\string stBtn2\string stBtn3\string stBtn4\string stBtn5,icondata icIcon)
        VAR num nAnswer;
        VAR string stMsg{5};
        VAR string stBtn{5};
        VAR string stAnswer;
        !
        ! Initialize variables 
        stMsg:=["","","","",""];
        stBtn:=["","","","",""];
        !
        ! Load meassge 
        stMsg{1}:=stMsgL1;
        IF Present(stMsgL2) stMsg{2}:=stMsgL2;
        IF Present(stMsgL3) stMsg{3}:=stMsgL3;
        IF Present(stMsgL4) stMsg{4}:=stMsgL4;
        IF Present(stMsgL5) stMsg{5}:=stMsgL5;
        !
        ! Load buttons
        stBtn{1}:=stBtn1;
        IF Present(stBtn2) stBtn{2}:=stBtn2;
        IF Present(stBtn3) stBtn{3}:=stBtn3;
        IF Present(stBtn4) stBtn{4}:=stBtn4;
        IF Present(stBtn5) stBtn{5}:=stBtn5;
        !
        ! Msg for user
        nAnswer:=UIMessageBox(
            \Header:=stMsgHeader
            \MsgArray:=stMsg
            \BtnArray:=stBtn
            \Icon:=icIcon);
        !
        ! handle user answer
        IF nAnswer=1 stAnswer:=stBtn{1};
        IF nAnswer=2 stAnswer:=stBtn{2};
        IF nAnswer=3 stAnswer:=stBtn{3};
        IF nAnswer=4 stAnswer:=stBtn{4};
        IF nAnswer=5 stAnswer:=stBtn{5};
        !
        ! Return user answer as string
        RETURN stAnswer;
    ERROR
        ! Placeholder for Error Code...
    ENDFUNC

    !************************************************
    ! Function    :     User interface numerical entry
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.06
    ! **************** ETH Zürich *******************
    !
    FUNC num f_A042_UINumEntry(string stMsgHeader,string stMsgL1,\string stMsgL2,\string stMsgL3,\string stMsgL4,\string stMsgL5,num nMin,num nMax,\num nDefault,icondata icIcon)
        VAR string stMsg{5};
        VAR num nAnswer;
        VAR num nInitValue;
        !
        ! Initialize variables 
        stMsg:=["","","","",""];
        nInitValue:=nMin;
        !
        ! Load meassge 
        stMsg{1}:=stMsgL1;
        IF Present(stMsgL2) stMsg{2}:=stMsgL2;
        IF Present(stMsgL3) stMsg{3}:=stMsgL3;
        IF Present(stMsgL4) stMsg{4}:=stMsgL4;
        IF Present(stMsgL5) stMsg{5}:=stMsgL5;
        !
        ! Use default value when present 
        IF Present(nDefault) nInitValue:=nDefault;
        !
        ! Msg for user
        nAnswer:=Round(UINumEntry(
            \Header:=stMsgHeader
            \MsgArray:=stMsg
            \Icon:=icIcon
            \InitValue:=nInitValue
            \MinValue:=nMin
            \MaxValue:=nMax)\Dec:=1);
        !
        ! Return user answer as string
        RETURN nAnswer;
    ERROR
        ! Placeholder for Error Code...
    ENDFUNC


ENDMODULE