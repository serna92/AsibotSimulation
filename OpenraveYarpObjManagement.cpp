/**
 * thanks Rosen Diankov
   Every plugin contains a bunch of openrave interfaces, the plugincpp plugin creates a simple OpenRAVE::ModuleBase interface named \b mymodule.
   Inside programs, load the plugin using the RaveLoadPlugin, and then create the module the plugin offers using
   \verbatim
   m=RaveCreateModule(env,"mymodule");
   \endverbatim
   To test things through the command line, do:
   \verbatim
   openrave --loadplugin libplugincpp.so --module mymodule "my args"
   \endverbatim
   This will load liboplugincpp.so and startup module "mymodule". From plugincpp, notice that mymodule
   supports some "commands". These are in-process string-based calls invoked through
   interface->SendCommand function.
   If you are using octave or matlab, then can communicate with openrave through tcp/ip, check out: http://openrave.programmingvision.com/wiki/index.php/OctaveMATLAB
   Most openrave users use python to dynamically interact with openrave. For example:
   \verbatim
   openrave.py -i  --loadplugin libplugincpp.so data/lab1.env.xml
   \endverbatim
   drops into the python promp with the plugin loaded and a scene loaded. Then it is possible to execute the following python commands to create the interface and call a command:
   \verbatim
   m=RaveCreateModule(env,'mymodule')
   env.Add(m,true,'my args')
   m.SendCommand('numbodies')
   \endverbatim
   <b>Full Example Code:</b>
 */
#include <openrave/openrave.h>
#include <openrave/plugin.h>
#include <boost/bind.hpp>

#include <yarp/os/all.h>
#include <yarp/dev/all.h>

#define DIMENSIONS 2


using namespace std;
using namespace OpenRAVE;

class DataProcessor : public yarp::os::PortReader {

public:

    void setPosition(vector<double>* position, KinBodyPtr _objPtr) {
        //_objPtr->position = position;
    }
    void setVisibility(bool visible, KinBodyPtr _objPtr) {
        _objPtr->SetVisible(visible);
    }
    void setObjects(KinBodyPtr _redCanPtr, KinBodyPtr _bottlePtr, KinBodyPtr _glassPtr, KinBodyPtr _dishPtr) {
        
	this->_redCanPtr = _redCanPtr;
	this->_bottlePtr = _bottlePtr;
	this->_glassPtr = _glassPtr;
	this->_dishPtr = _dishPtr;
    }

private:

    vector<double>* position;
    bool visible;
    KinBodyPtr _redCanPtr, _bottlePtr, _glassPtr, _dishPtr;

    virtual bool read(yarp::os::ConnectionReader& in)
    {
        yarp::os::Bottle request, response;
        if (!request.read(in)) return false;
        printf("Request: %s\n", request.toString().c_str());
        yarp::os::ConnectionWriter *out = in.getWriter();
        if (out==NULL) return true;

        //--
        if ( request.get(0).asString() == "getposition" )
        {
        /*    for(int i=0; i<position->size();i++)
                response.adddouble(position->operator[](i));*/

            return response.write(*out);
        }
        else if ( request.get(0).asString() == "setposition" )
        {

            for(int i=0; i<position->size();i++)
                position->operator[](i) = request.get(i+1).asDouble();

            response.addString("ok");
            return response.write(*out);
        }
        else if ( request.get(0).asString() == "setvisible" )
        {
	    visible = request.get(2).asBool();

 	    if ( request.get(1).asString() == "redCan" )
		setVisibility(visible, _redCanPtr);

	    else if ( request.get(1).asString() == "dish" )
		setVisibility(visible, _dishPtr);

	    else if ( request.get(1).asString() == "glass" )
		setVisibility(visible, _glassPtr);
		
	    else if ( request.get(1).asString() == "bottle" )
	    	setVisibility(visible, _bottlePtr);

            response.addString("ok");
            return response.write(*out);
        }

        response.addString("unknown command");
        return response.write(*out);
    }


};

class OpenraveYarpObjManagement : public ModuleBase
{
public:
    OpenraveYarpObjManagement(EnvironmentBasePtr penv) : ModuleBase(penv) {
        __description = "OpenraveYarpObjManagement plugin.";
        RegisterCommand("open",boost::bind(&OpenraveYarpObjManagement::Open, this,_1,_2),"opens port");
    }

    virtual ~OpenraveYarpObjManagement() {
        rpcServer.close();
    }

    virtual void Destroy() {

        RAVELOG_INFO("module unloaded from environment\n");
    }

    bool Open(ostream& sout, istream& sinput)
    {
        vector<string> funcionArgs;
        while(sinput)
        {
            string funcionArg;
            sinput >> funcionArg;
            funcionArgs.push_back(funcionArg);
        }

        string portName("/openraveObjManagement/rpc:s");

        if (funcionArgs.size() > 0)
        {
            if( funcionArgs[0][0] == '/')
                portName = funcionArgs[0];
        }
        RAVELOG_INFO("portName: %s\n",portName.c_str());

        if ( !yarp.checkNetwork() )
        {
            RAVELOG_INFO("Found no yarp network (try running \"yarpserver &\"), bye!\n");
            return false;
        }

        RAVELOG_INFO("penv: %p\n",GetEnv().get());
        OpenRAVE::EnvironmentBasePtr penv = GetEnv();

	_redCanPtr = penv->GetKinBody("redCan");
        if(!_redCanPtr) {
            fprintf(stderr,"error: object \"redCan\" does not exist.\n");
        } else printf("sucess: object \"redCan\" exists.\n");	

        _bottlePtr = penv->GetKinBody("bottle");
        if(!_bottlePtr) {
            fprintf(stderr,"error: object \"bottle\" does not exist.\n");
        } else printf("sucess: object \"bottle\" exists.\n");

        _glassPtr = penv->GetKinBody("glass");
        if(!_glassPtr) {
            fprintf(stderr,"error: object \"glass\" does not exist.\n");
        } else printf("sucess: object \"glass\" exists.\n");

        _dishPtr = penv->GetKinBody("dish");
        if(!_dishPtr) {
            fprintf(stderr,"error: object \"dish\" does not exist.\n");
        } else printf("sucess: object \"dish\" exists.\n");


        //position.resize(DIMENSIONS);

        processor.setObjects(_redCanPtr, _bottlePtr, _glassPtr, _dishPtr);
        rpcServer.setReader(processor);
        rpcServer.open(portName);

        return true;
    }

/*    virtual void run()
    {
        //RAVELOG_INFO("thread\n");

        //Get new object (pen) position
        T_base_object = _objPtr->GetTransform();
        double T_base_object_x = T_base_object.trans.x;
        double T_base_object_y = T_base_object.trans.y;
        double T_base_object_z = T_base_object.trans.z;

        //Update psqpainted to the new values
        for(int i=0; i<(sqPainted.size()); i++)
        {
            stringstream ss;
            ss << "square" << i;
            Transform pos_square = _wall->GetLink(ss.str())->GetGeometry(0)->GetTransform();

            double pos_square_x = pos_square.trans.x;
            double pos_square_y = pos_square.trans.y;
            double pos_square_z = pos_square.trans.z;
            double dist = sqrt(pow(T_base_object_x-pos_square_x,2)
                                      + pow(T_base_object_y-pos_square_y,2)
                                      + pow(T_base_object_z-pos_square_z,2) );

            if (dist < 0.13)
            {
                sqPaintedSemaphore.wait();
                sqPainted[i]=1;
                sqPaintedSemaphore.post();
            }

            sqPaintedSemaphore.wait();
            int sqPaintedValue = sqPainted[i];
            sqPaintedSemaphore.post();

            if( sqPaintedValue == 1 )
            {
                _wall->GetLink(ss.str())->GetGeometry(0)->SetDiffuseColor(RaveVector<float>(0.0, 0.0, 1.0));
            }
            else
            {
                _wall->GetLink(ss.str())->GetGeometry(0)->SetDiffuseColor(RaveVector<float>(0.5, 0.5, 0.5));
            }

        }

    }*/

private:
    yarp::os::Network yarp;
    yarp::os::RpcServer rpcServer;
    DataProcessor processor;
    KinBodyPtr _redCanPtr, _bottlePtr, _glassPtr, _dishPtr;
};

InterfaceBasePtr CreateInterfaceValidated(InterfaceType type, const std::string& interfacename, std::istream& sinput, EnvironmentBasePtr penv) {
    if( type == PT_Module && interfacename == "openraveyarpobjmanagement" ) {
        return InterfaceBasePtr(new OpenraveYarpObjManagement(penv));
    }
    return InterfaceBasePtr();
}

void GetPluginAttributesValidated(PLUGININFO& info) {
    info.interfacenames[PT_Module].push_back("OpenraveYarpObjManagement");
}

OPENRAVE_PLUGIN_API void DestroyPlugin() {
    RAVELOG_INFO("destroying plugin\n");
}
