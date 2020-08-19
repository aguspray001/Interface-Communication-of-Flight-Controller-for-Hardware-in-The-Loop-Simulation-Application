import thread, time

def input_thread(L):
    raw_input()
    L.append(None)
    
def do_print():
    L = []
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(.1)
        if L: break
        print "Hi Mom!"
        
do_print()
