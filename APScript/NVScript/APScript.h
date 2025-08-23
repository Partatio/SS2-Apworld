#ifndef APSCRIPTS_H
#define APSCRIPTS_H
#endif

#pragma once

#include "scriptvars.h"
#include "ScriptNV.h"

DECLARE_SCRIPT(cScr_APLocation,cScriptNV)
{
public:
	DECLARE_FACTORY(APLocation,CustomScript);
	cScr_APLocation(const char* pszName, int iHostObjId)
		: cScriptNV(pszName,iHostObjId)
	{ }

private:
	DECLARE_MSGHANDLER(OnFrobWorldEnd);

protected:
	virtual void InitScriptData()
	{
		cScriptNV::InitScriptData();
		REGISTER_MSGHANDLER("FrobWorldEnd", cScr_APLocation::OnFrobWorldEnd);
	}
}
END_DECLARE_SCRIPT(cScr_APLocation);