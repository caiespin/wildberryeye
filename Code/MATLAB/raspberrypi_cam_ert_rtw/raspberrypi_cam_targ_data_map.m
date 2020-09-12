  function targMap = targDataMap(),

  ;%***********************
  ;% Create Parameter Map *
  ;%***********************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 3;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc paramMap
    ;%
    paramMap.nSections           = nTotSects;
    paramMap.sectIdxOffset       = sectIdxOffset;
      paramMap.sections(nTotSects) = dumSection; %prealloc
    paramMap.nTotData            = -1;
    
    ;%
    ;% Auto data (eahe20cjf0)
    ;%
      section.nData     = 2;
      section.data(2)  = dumData; %prealloc
      
	  ;% eahe20cjf0.Out1_Y0
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% eahe20cjf0.Constant_Value
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 1;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(1) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% eahe20cjf0.Memory_InitialCondition
	  section.data(1).logicalSrcIdx = 2;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(2) = section;
      clear section
      
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% eahe20cjf0.Constant_Value_pqka2xpeql
	  section.data(1).logicalSrcIdx = 3;
	  section.data(1).dtTransOffset = 0;
	
	  ;% eahe20cjf0.UnitDelay_InitialCondition
	  section.data(2).logicalSrcIdx = 4;
	  section.data(2).dtTransOffset = 1;
	
	  ;% eahe20cjf0.Constant1_Value
	  section.data(3).logicalSrcIdx = 5;
	  section.data(3).dtTransOffset = 2;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(3) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (parameter)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    paramMap.nTotData = nTotData;
    


  ;%**************************
  ;% Create Block Output Map *
  ;%**************************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 5;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc sigMap
    ;%
    sigMap.nSections           = nTotSects;
    sigMap.sectIdxOffset       = sectIdxOffset;
      sigMap.sections(nTotSects) = dumSection; %prealloc
    sigMap.nTotData            = -1;
    
    ;%
    ;% Auto data (i40k2uujetv)
    ;%
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% i40k2uujetv.oi3yl3c1ql
	  section.data(1).logicalSrcIdx = 5;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(1) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% i40k2uujetv.psa35ghqnt
	  section.data(1).logicalSrcIdx = 6;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(2) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% i40k2uujetv.ftdtq2wyf1
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(3) = section;
      clear section
      
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% i40k2uujetv.argflqhh3w
	  section.data(1).logicalSrcIdx = 1;
	  section.data(1).dtTransOffset = 0;
	
	  ;% i40k2uujetv.msk30yohwd
	  section.data(2).logicalSrcIdx = 2;
	  section.data(2).dtTransOffset = 480000;
	
	  ;% i40k2uujetv.dwrt5t3jgg
	  section.data(3).logicalSrcIdx = 3;
	  section.data(3).dtTransOffset = 960000;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(4) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% i40k2uujetv.gin2ownkth
	  section.data(1).logicalSrcIdx = 4;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(5) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (signal)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    sigMap.nTotData = nTotData;
    


  ;%*******************
  ;% Create DWork Map *
  ;%*******************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 8;
    sectIdxOffset = 5;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc dworkMap
    ;%
    dworkMap.nSections           = nTotSects;
    dworkMap.sectIdxOffset       = sectIdxOffset;
      dworkMap.sections(nTotSects) = dumSection; %prealloc
    dworkMap.nTotData            = -1;
    
    ;%
    ;% Auto data (ogj15alfnt4)
    ;%
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.nvr34stgxk
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(1) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.cpezzo1ngr
	  section.data(1).logicalSrcIdx = 1;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(2) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.aqwjmxblfc.LoggedData
	  section.data(1).logicalSrcIdx = 2;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(3) = section;
      clear section
      
      section.nData     = 26;
      section.data(26)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.ipa1raccsd
	  section.data(1).logicalSrcIdx = 3;
	  section.data(1).dtTransOffset = 0;
	
	  ;% ogj15alfnt4.esxecqjokf
	  section.data(2).logicalSrcIdx = 4;
	  section.data(2).dtTransOffset = 2;
	
	  ;% ogj15alfnt4.immxgwjz0p
	  section.data(3).logicalSrcIdx = 5;
	  section.data(3).dtTransOffset = 4;
	
	  ;% ogj15alfnt4.pbztxqtlo2
	  section.data(4).logicalSrcIdx = 6;
	  section.data(4).dtTransOffset = 6;
	
	  ;% ogj15alfnt4.ip3e3bfjdj
	  section.data(5).logicalSrcIdx = 7;
	  section.data(5).dtTransOffset = 8;
	
	  ;% ogj15alfnt4.dpeqbtvmw0
	  section.data(6).logicalSrcIdx = 8;
	  section.data(6).dtTransOffset = 10;
	
	  ;% ogj15alfnt4.phdebz2r1r
	  section.data(7).logicalSrcIdx = 9;
	  section.data(7).dtTransOffset = 12;
	
	  ;% ogj15alfnt4.gpcbffcgzk
	  section.data(8).logicalSrcIdx = 10;
	  section.data(8).dtTransOffset = 22;
	
	  ;% ogj15alfnt4.hgnofe3tl4
	  section.data(9).logicalSrcIdx = 11;
	  section.data(9).dtTransOffset = 32;
	
	  ;% ogj15alfnt4.fodp0xakz0
	  section.data(10).logicalSrcIdx = 12;
	  section.data(10).dtTransOffset = 34;
	
	  ;% ogj15alfnt4.medxucvuuo
	  section.data(11).logicalSrcIdx = 13;
	  section.data(11).dtTransOffset = 36;
	
	  ;% ogj15alfnt4.igtt2l2qrp
	  section.data(12).logicalSrcIdx = 14;
	  section.data(12).dtTransOffset = 38;
	
	  ;% ogj15alfnt4.i0ntxscjn4
	  section.data(13).logicalSrcIdx = 15;
	  section.data(13).dtTransOffset = 40;
	
	  ;% ogj15alfnt4.krckw2aqsl
	  section.data(14).logicalSrcIdx = 16;
	  section.data(14).dtTransOffset = 42;
	
	  ;% ogj15alfnt4.jii1mivn2u
	  section.data(15).logicalSrcIdx = 17;
	  section.data(15).dtTransOffset = 44;
	
	  ;% ogj15alfnt4.a3mv5yyki2
	  section.data(16).logicalSrcIdx = 18;
	  section.data(16).dtTransOffset = 46;
	
	  ;% ogj15alfnt4.on0mywcl14
	  section.data(17).logicalSrcIdx = 19;
	  section.data(17).dtTransOffset = 48;
	
	  ;% ogj15alfnt4.fkwwvlort2
	  section.data(18).logicalSrcIdx = 20;
	  section.data(18).dtTransOffset = 50;
	
	  ;% ogj15alfnt4.kusj3e1whp
	  section.data(19).logicalSrcIdx = 21;
	  section.data(19).dtTransOffset = 52;
	
	  ;% ogj15alfnt4.hfr4sfnmzq
	  section.data(20).logicalSrcIdx = 22;
	  section.data(20).dtTransOffset = 54;
	
	  ;% ogj15alfnt4.ctfzcqvtvn
	  section.data(21).logicalSrcIdx = 23;
	  section.data(21).dtTransOffset = 64;
	
	  ;% ogj15alfnt4.hx4ec0zi2z
	  section.data(22).logicalSrcIdx = 24;
	  section.data(22).dtTransOffset = 74;
	
	  ;% ogj15alfnt4.ow41euskfo
	  section.data(23).logicalSrcIdx = 25;
	  section.data(23).dtTransOffset = 76;
	
	  ;% ogj15alfnt4.kka0tadevn
	  section.data(24).logicalSrcIdx = 26;
	  section.data(24).dtTransOffset = 78;
	
	  ;% ogj15alfnt4.ondgay5aiw
	  section.data(25).logicalSrcIdx = 27;
	  section.data(25).dtTransOffset = 80;
	
	  ;% ogj15alfnt4.kkhdnjdtsb
	  section.data(26).logicalSrcIdx = 28;
	  section.data(26).dtTransOffset = 82;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(4) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.e3rmesxa13
	  section.data(1).logicalSrcIdx = 29;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(5) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.mpzd10wn1n
	  section.data(1).logicalSrcIdx = 30;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(6) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.m50ovu1alu
	  section.data(1).logicalSrcIdx = 31;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(7) = section;
      clear section
      
      section.nData     = 5;
      section.data(5)  = dumData; %prealloc
      
	  ;% ogj15alfnt4.ftu1wzxryp
	  section.data(1).logicalSrcIdx = 32;
	  section.data(1).dtTransOffset = 0;
	
	  ;% ogj15alfnt4.pfra1oyfy5
	  section.data(2).logicalSrcIdx = 33;
	  section.data(2).dtTransOffset = 1;
	
	  ;% ogj15alfnt4.f4jerhhs2z
	  section.data(3).logicalSrcIdx = 34;
	  section.data(3).dtTransOffset = 3;
	
	  ;% ogj15alfnt4.ewl1zamdqh
	  section.data(4).logicalSrcIdx = 35;
	  section.data(4).dtTransOffset = 5;
	
	  ;% ogj15alfnt4.kerxjpeuf1
	  section.data(5).logicalSrcIdx = 36;
	  section.data(5).dtTransOffset = 6;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(8) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (dwork)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    dworkMap.nTotData = nTotData;
    


  ;%
  ;% Add individual maps to base struct.
  ;%

  targMap.paramMap  = paramMap;    
  targMap.signalMap = sigMap;
  targMap.dworkMap  = dworkMap;
  
  ;%
  ;% Add checksums to base struct.
  ;%


  targMap.checksum0 = 1497136862;
  targMap.checksum1 = 3325034669;
  targMap.checksum2 = 2718542928;
  targMap.checksum3 = 3176994187;

