"""
MFRC522 RFID/NFC Reader Driver
Based on the MFRC522 library for Raspberry Pi
"""

import spidev
import signal
import time


class MFRC522:
    """Driver for MFRC522 RFID/NFC reader module"""
    
    # MFRC522 registers
    CommandReg = 0x01
    ComIEnReg = 0x02
    DivIEnReg = 0x03
    ComIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E
    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxASKReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19
    MfTxReg = 0x1C
    MfRxReg = 0x1D
    SerialSpeedReg = 0x1F
    CRCResultRegM = 0x21
    CRCResultRegL = 0x22
    ModWidthReg = 0x24
    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    TCounterValueRegH = 0x2E
    TCounterValueRegL = 0x2F
    TestSel1Reg = 0x31
    TestSel2Reg = 0x32
    TestPinEnReg = 0x33
    TestPinValueReg = 0x34
    TestBusReg = 0x35
    AutoTestReg = 0x36
    VersionReg = 0x37
    AnalogTestReg = 0x38
    TestDAC1Reg = 0x39
    TestDAC2Reg = 0x3A
    TestADCReg = 0x3B
    
    # MFRC522 commands
    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03
    
    # PICC commands
    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SElECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ = 0x30
    PICC_WRITE = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE = 0xC2
    PICC_TRANSFER = 0xB0
    PICC_HALT = 0x50
    
    # Status codes
    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2
    
    def __init__(self, bus=0, device=0, spd=1000000, pin_mode=10, pin_rst=22, debugLevel='WARNING'):
        """
        Initialize MFRC522 reader
        
        Args:
            bus: SPI bus (default 0)
            device: SPI device (default 0)
            spd: SPI speed in Hz (default 1MHz)
            pin_mode: Not used, kept for compatibility
            pin_rst: GPIO pin for reset (default 22)
            debugLevel: Logging level
        """
        import RPi.GPIO as GPIO
        self.GPIO = GPIO
        
        self.RESET = pin_rst
        
        # Setup GPIO
        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setup(self.RESET, GPIO.OUT)
        self.GPIO.output(self.RESET, 1)
        
        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = spd
        
        # Initialize the reader
        self.MFRC522_Init()
    
    def MFRC522_Reset(self):
        """Soft reset the MFRC522"""
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)
    
    def Write_MFRC522(self, addr, val):
        """Write a byte to MFRC522 register"""
        self.spi.xfer2([(addr << 1) & 0x7E, val])
    
    def Read_MFRC522(self, addr):
        """Read a byte from MFRC522 register"""
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return val[1]
    
    def SetBitMask(self, reg, mask):
        """Set bit mask in register"""
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp | mask)
    
    def ClearBitMask(self, reg, mask):
        """Clear bit mask in register"""
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp & (~mask))
    
    def AntennaOn(self):
        """Turn on the antenna"""
        temp = self.Read_MFRC522(self.TxControlReg)
        if ~(temp & 0x03):
            self.SetBitMask(self.TxControlReg, 0x03)
    
    def AntennaOff(self):
        """Turn off the antenna"""
        self.ClearBitMask(self.TxControlReg, 0x03)
    
    def MFRC522_Init(self):
        """Initialize the MFRC522"""
        self.MFRC522_Reset()
        
        self.Write_MFRC522(self.TModeReg, 0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL, 30)
        self.Write_MFRC522(self.TReloadRegH, 0)
        
        self.Write_MFRC522(self.TxASKReg, 0x40)
        self.Write_MFRC522(self.ModeReg, 0x3D)
        
        self.AntennaOn()
    
    def MFRC522_Request(self, reqMode):
        """
        Request a card
        
        Args:
            reqMode: Request mode (PICC_REQIDL or PICC_REQALL)
            
        Returns:
            (status, backData): Status and card type data
        """
        status = None
        backBits = None
        TagType = []
        
        self.Write_MFRC522(self.BitFramingReg, 0x07)
        
        TagType.append(reqMode)
        (status, backData, backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, TagType)
        
        if ((status != self.MI_OK) | (backBits != 0x10)):
            status = self.MI_ERR
        
        return (status, backBits)
    
    def MFRC522_ToCard(self, command, sendData):
        """
        Communicate with card
        
        Args:
            command: MFRC522 command
            sendData: Data to send
            
        Returns:
            (status, backData, backLen): Status, response data, and response length
        """
        backData = []
        backLen = 0
        status = self.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0
        
        if command == self.PCD_AUTHENT:
            irqEn = 0x12
            waitIRq = 0x10
        if command == self.PCD_TRANSCEIVE:
            irqEn = 0x77
            waitIRq = 0x30
        
        self.Write_MFRC522(self.ComIEnReg, irqEn | 0x80)
        self.ClearBitMask(self.ComIrqReg, 0x80)
        self.SetBitMask(self.FIFOLevelReg, 0x80)
        
        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE)
        
        for i in range(len(sendData)):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])
        
        self.Write_MFRC522(self.CommandReg, command)
        
        if command == self.PCD_TRANSCEIVE:
            self.SetBitMask(self.BitFramingReg, 0x80)
        
        i = 2000
        while True:
            n = self.Read_MFRC522(self.ComIrqReg)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):
                break
        
        self.ClearBitMask(self.BitFramingReg, 0x80)
        
        if i != 0:
            if (self.Read_MFRC522(self.ErrorReg) & 0x1B) == 0x00:
                status = self.MI_OK
                
                if n & irqEn & 0x01:
                    status = self.MI_NOTAGERR
                
                if command == self.PCD_TRANSCEIVE:
                    n = self.Read_MFRC522(self.FIFOLevelReg)
                    lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
                    if lastBits != 0:
                        backLen = (n - 1) * 8 + lastBits
                    else:
                        backLen = n * 8
                    
                    if n == 0:
                        n = 1
                    if n > 16:
                        n = 16
                    
                    for i in range(n):
                        backData.append(self.Read_MFRC522(self.FIFODataReg))
            else:
                status = self.MI_ERR
        
        return (status, backData, backLen)
    
    def MFRC522_Anticoll(self):
        """
        Anti-collision detection, read card serial number
        
        Returns:
            (status, uid): Status and card UID
        """
        backData = []
        serNumCheck = 0
        
        serNum = []
        
        self.Write_MFRC522(self.BitFramingReg, 0x00)
        
        serNum.append(self.PICC_ANTICOLL)
        serNum.append(0x20)
        
        (status, backData, backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, serNum)
        
        if status == self.MI_OK:
            if len(backData) == 5:
                for i in range(4):
                    serNumCheck = serNumCheck ^ backData[i]
                if serNumCheck != backData[4]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR
        
        return (status, backData)
    
    def CalulateCRC(self, pIndata):
        """Calculate CRC using MFRC522"""
        self.ClearBitMask(self.DivIrqReg, 0x04)
        self.SetBitMask(self.FIFOLevelReg, 0x80)
        
        for i in range(len(pIndata)):
            self.Write_MFRC522(self.FIFODataReg, pIndata[i])
        
        self.Write_MFRC522(self.CommandReg, self.PCD_CALCCRC)
        
        i = 0xFF
        while True:
            n = self.Read_MFRC522(self.DivIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break
        
        pOutData = []
        pOutData.append(self.Read_MFRC522(self.CRCResultRegL))
        pOutData.append(self.Read_MFRC522(self.CRCResultRegM))
        return pOutData
    
    def MFRC522_SelectTag(self, serNum):
        """Select a card"""
        backData = []
        buf = []
        buf.append(self.PICC_SElECTTAG)
        buf.append(0x70)
        
        for i in range(5):
            buf.append(serNum[i])
        
        pOut = self.CalulateCRC(buf)
        buf.append(pOut[0])
        buf.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buf)
        
        if (status == self.MI_OK) and (backLen == 0x18):
            return backData[0]
        else:
            return 0
    
    def MFRC522_Auth(self, authMode, BlockAddr, Sectorkey, serNum):
        """Authenticate card"""
        buff = []
        
        buff.append(authMode)
        buff.append(BlockAddr)
        
        for i in range(len(Sectorkey)):
            buff.append(Sectorkey[i])
        
        for i in range(4):
            buff.append(serNum[i])
        
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_AUTHENT, buff)
        
        if not (status == self.MI_OK):
            print("AUTH ERROR!!")
        if not (self.Read_MFRC522(self.Status2Reg) & 0x08) != 0:
            print("AUTH ERROR(status2reg & 0x08) != 0")
        
        return status
    
    def MFRC522_StopCrypto1(self):
        """Stop crypto1 encryption"""
        self.ClearBitMask(self.Status2Reg, 0x08)
    
    def MFRC522_Read(self, blockAddr):
        """Read a block from the card"""
        recvData = []
        recvData.append(self.PICC_READ)
        recvData.append(blockAddr)
        pOut = self.CalulateCRC(recvData)
        recvData.append(pOut[0])
        recvData.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, recvData)
        if not (status == self.MI_OK):
            print("Error while reading!")
        
        if len(backData) == 16:
            return backData
        else:
            return None
    
    def MFRC522_Write(self, blockAddr, writeData):
        """Write a block to the card"""
        buff = []
        buff.append(self.PICC_WRITE)
        buff.append(blockAddr)
        crc = self.CalulateCRC(buff)
        buff.append(crc[0])
        buff.append(crc[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buff)
        if not (status == self.MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
            status = self.MI_ERR
        
        if status == self.MI_OK:
            buf = []
            for i in range(16):
                buf.append(writeData[i])
            
            crc = self.CalulateCRC(buf)
            buf.append(crc[0])
            buf.append(crc[1])
            (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buf)
            if not (status == self.MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
                print("Error while writing")
        
        return status
    
    def MFRC522_DumpClassic1K(self, key, uid):
        """Dump all blocks from MIFARE Classic 1K card"""
        for i in range(64):
            status = self.MFRC522_Auth(self.PICC_AUTHENT1A, i, key, uid)
            if status == self.MI_OK:
                data = self.MFRC522_Read(i)
                if data:
                    print(f"Block {i}: {' '.join([f'{x:02X}' for x in data])}")
            else:
                print(f"Authentication error on block {i}")
    
    def close(self):
        """Clean up resources"""
        self.spi.close()
        self.GPIO.cleanup()

