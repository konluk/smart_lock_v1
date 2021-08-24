from website import create_app
#from smartlock import main_smartlock
import _thread as thread


app = create_app()


if __name__ == '__main__':   
    
    #thread.start_new_thread( main_smartlock.create_smartlock, () )
    app.run(debug=False,host='0.0.0.0', threaded=True) #debug - po zmene v kode sa aktualizuje server
    
