//////////////////////////////////////////////////////////////////////////
// Mapper177  HengGe                                                    //
//////////////////////////////////////////////////////////////////////////
void    Mapper177::Reset()
{
	SetPROM_32K_Bank( 0 );
	HengGe_TYPE = 0;
	DWORD	crc = nes->rom->GetPROM_CRC();
	if( crc == 0x02c41438 ) {	// Xing He Zhan Shi (C)
		HengGe_TYPE = 1;
	}
}

void	Mapper177::WriteLow( WORD addr, BYTE data )
{
		if( HengGe_TYPE == 1 ) {
			if(addr==0x5ff1){
				SetPROM_32K_Bank( (data>>1));
			}
		}
		if( addr>=0x6000 ) {
			CPU_MEM_BANK[addr>>13][addr&0x1FFF] = data;
		}
}

void	Mapper177::Write( WORD addr, BYTE data )
{
		if( HengGe_TYPE == 0 ) {
			SetPROM_32K_Bank( data );
			if( data&0x20 ) SetVRAM_Mirror( VRAM_HMIRROR );
			else			SetVRAM_Mirror( VRAM_VMIRROR );
		}
		if( HengGe_TYPE == 1) {
			if(addr==0xa000){
				if( data & 0x01 ) SetVRAM_Mirror( VRAM_HMIRROR );
					else		  SetVRAM_Mirror( VRAM_VMIRROR );
			}
			if(addr==0xa001){
				//unknown
			}
		}
}

