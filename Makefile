CC = cc
CFLAGS = -Wall -Wno-unused-variable \
         $(shell pkg-config --cflags json-c libusb-1.0)
LDFLAGS = $(shell pkg-config --libs json-c libusb-1.0)

SRCDIR = src/libs
TOOLDIR = src/umtool

LIB_SRCS = $(SRCDIR)/ultimarc.c $(SRCDIR)/common.c $(SRCDIR)/ulboard.c \
           $(SRCDIR)/ipac.c $(SRCDIR)/ipacseries.c $(SRCDIR)/ipacultimate.c \
           $(SRCDIR)/pacLED.c $(SRCDIR)/pacdrive.c $(SRCDIR)/ultrastik.c \
           $(SRCDIR)/usbbutton.c $(SRCDIR)/servostik.c $(SRCDIR)/uhid.c
TOOL_SRCS = $(TOOLDIR)/main.c

LIB_OBJS = $(LIB_SRCS:.c=.o)
TOOL_OBJS = $(TOOL_SRCS:.c=.o)

TARGET = umtool

all: $(TARGET)

$(TARGET): $(LIB_OBJS) $(TOOL_OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

$(SRCDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -I$(SRCDIR) -c -o $@ $<

$(TOOLDIR)/%.o: $(TOOLDIR)/%.c
	$(CC) $(CFLAGS) -Isrc -c -o $@ $<

clean:
	rm -f $(LIB_OBJS) $(TOOL_OBJS) $(TARGET)

.PHONY: all clean
