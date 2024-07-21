#pragma once
#ifdef GAME_PROFILE_EXPORTS
#define GAME_PROFILE_API __declspec( dllexport )
#else
#define GAME_PROFILE_API __declspec( dllimport )
#endif

class IGameProfileSys
{
public:
	virtual ~IGameProfileSys() { }
	virtual void addCallProfile(const int id, const int time, const int start_index) = 0;

	virtual void start() = 0;

	virtual void dump2File(int index) = 0;

	virtual int getCurIndex() = 0;
};

extern "C" GAME_PROFILE_API IGameProfileSys* GetProfileSys();

