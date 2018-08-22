//////////////////////////////////////////////////////////////////////////
// Mapper176                                                            //
//////////////////////////////////////////////////////////////////////////
void	Mapper176::Reset()
{
	SetPROM_32K_Bank( 0, 1, PROM_8K_SIZE-2, PROM_8K_SIZE-1 );
	if( VROM_1K_SIZE ) {
		SetVROM_8K_Bank( 0 );
	}
}

void	Mapper176::WriteLow( WORD addr, BYTE data )
{
	switch( addr ) {
		case 0x5ff1:
			 SetPROM_32K_Bank( data>>1 );
			 break;
		case 0x5ff2:
			 SetVROM_8K_Bank( data );
			 break;
		default:
			 break;
			 }
	if( addr>=0x6000 ) {
		CPU_MEM_BANK[addr>>13][addr&0x1FFF] = data;
	}
}

