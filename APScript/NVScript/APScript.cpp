#include <cstdio>

#include "lg/interface.h"
#include "lg/scrservices.h"
#include "lg/scrmanagers.h"
#include "lg/scrmsgs.h"
#include "lg/objects.h"
#include "ScriptLib.h"

#define INITOSM
#include "APScript.h"

#include "lg/iids.h"

MSGHANDLER cScr_APLocation::OnFrobWorldEnd(sScrMsg* pMsg, sMultiParm* pReply, eScrTraceAction eTrace)
{
	SService<IPropertySrv> pPropSrv(g_pScriptManager);

	pPropSrv->Set(m_iObjId, "FrobInfo", "World Action", 18);
	FILE *fp;
	fp = std::fopen("APcommunications/SentItems.txt", "a");
	cMultiParm apid;
	pPropSrv->Get(apid, m_iObjId, "VoiceIdx", NULL);
	int apidint = apid.i;
	fprintf(fp, "%i,", apidint);
	fclose(fp);

	return 0;
}