MODULE A042_DataRecord
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
    ! FUNCTION    :  Includ all data records
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

    RECORD A042_channel
        A042_channeldata Ch_1;
        A042_channeldata Ch_2;
        A042_channeldata Ch_3;
        A042_channeldata Ch_4;
    ENDRECORD

    RECORD A042_channeldata
        string T_Name;
        num Ch_Nr;
    ENDRECORD

    RECORD A042_Protocol
        A042_Header ProtocolHeader;
        A042_Data ProtocolData;
    ENDRECORD

    RECORD A042_Header
        num M_Len;
        num Ver;
        num TS_Sec;
        num TS_NSec;
    ENDRECORD

    RECORD A042_Data
        num S_ID;
        num E_Lev;
        num I_Len;
        string Instr;
        num F_Lev;
        num F_Len;
        string Feedb;
        num F_ID;
        num St_Cnt;
        num St1_Len;
        string St1;
        num St2_Len;
        string St2;
        num St3_Len;
        string St3;
        num St4_Len;
        string St4;
        num St5_Len;
        string St5;
        num St6_Len;
        string St6;
        num St7_Len;
        string St7;
        num St8_Len;
        string St8;
        num V_Cnt;
        num V1;
        num V2;
        num V3;
        num V4;
        num V5;
        num V6;
        num V7;
        num V8;
        num V9;
        num V10;
        num V11;
        num V12;
        num V13;
        num V14;
        num V15;
        num V16;
        num V17;
        num V18;
        num V19;
        num V20;
        num V21;
        num V22;
        num V23;
        num V24;
        num V25;
        num V26;
        num V27;
        num V28;
        num V29;
        num V30;
        num V31;
        num V32;
        num V33;
        num V34;
        num V35;
        num V36;
    ENDRECORD

    RECORD A042_buffer_msg
        A042_Data Data;
        bool StartBit;
    ENDRECORD
ENDMODULE