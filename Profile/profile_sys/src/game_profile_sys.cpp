#include "../include/game_profile_sys.h"
#include "../third/pugixml.hpp"
#include <chrono>
#include <fstream>
#include <string>
#include <vector>
#include <Windows.h>

class CGameProfileSys : public IGameProfileSys
{
public:
	static CGameProfileSys& getInstance()
	{
		static CGameProfileSys profile_sys;
		return profile_sys;
	}
	struct TimeInfo {
		int time_cost = 0;
		int start_index = 0;
	};
	void addCallProfile(const int id, const int time, const int start_index)
	{
		if (m_working)
			++m_frame_call_times;
		if (m_working && time > m_wpr_cfg.marker_record_frame_time)
		{
			if (id == m_wpr_cfg.marker_frame_id)
			{
				m_profile_call_infos.push_back(std::make_pair(-999, TimeInfo{ m_frame_call_times, start_index }));
				m_frame_call_times = 0;
			}
			m_profile_call_infos.push_back(std::make_pair(id, TimeInfo{time, start_index}));
			if (m_wpr_cfg.open && time > m_wpr_cfg.marker_frame_time && id == m_wpr_cfg.marker_frame_id)
			{
				//m_wpr_cfg.marker_min_interval second add one mark
				auto now = std::chrono::system_clock::now();
				std::chrono::microseconds duration = std::chrono::duration_cast<std::chrono::microseconds>(now - m_mark_last);
				if (duration.count() > m_wpr_cfg.marker_min_interval)
				{
					m_mark_last = now;
					std::string wprMark = m_wpr_cfg.marker_cmd;
					wprMark = wprMark + std::to_string(time) + "_" + std::to_string(start_index);
					ShellExecuteA(NULL, "open", "cmd", wprMark.c_str(), 0, SW_HIDE);
				}
			}
		}

	}

	void start()
	{
		if (m_working)
			return;
		initCfg();
		m_working = true;
		if (m_wpr_cfg.open)
		{
			//"/c C:/wprTT.exe.lnk -start GeneralProfile -start CPU.verbose -start DiskIO.verbose -start FileIO.verbose "
			ShellExecuteA(NULL, "open", "cmd", m_wpr_cfg.start_cmd.c_str(), 0, SW_HIDE);
		}
	}

	void dump2File(int index)
	{
		if (!m_working)
			return;
		m_working = false;
		if (m_wpr_cfg.open)
		{
			std::string wpr_cmd = m_wpr_cfg.stop_cmd;// "/k C:/wprTT.exe.lnk -stop G:/profile_inner/";
			wpr_cmd = wpr_cmd + std::to_string(index) + ".etl";
			ShellExecuteA(NULL, "open", "cmd", wpr_cmd.c_str(), 0, SW_SHOW);
		}
		dumpFileImpl(index);
	}
	// Í¨¹ý IGameProfileSys ¼Ì³Ð
	int getCurIndex() override
	{
		return int(m_profile_call_infos.size());
	}

	void initCfg()
	{
		const char* file = "./game_profile_sys.xml";
		pugi::xml_document doc;
		auto ret = doc.load_file(file);
		if (!ret)
			return;
		auto root = doc.first_child();
		auto wpr = root.child("wpr");
		if (wpr)
		{
			m_wpr_cfg.open = wpr.child("open_wpr").text().as_bool(false);
			m_wpr_cfg.start_cmd = wpr.child("start").text().as_string();
			m_wpr_cfg.marker_cmd = wpr.child("marker").text().as_string();
			m_wpr_cfg.stop_cmd = wpr.child("stop").text().as_string();
			m_wpr_cfg.marker_min_interval = wpr.child("marker_min_interval").text().as_int();
			m_wpr_cfg.marker_frame_time = wpr.child("marker_frame_time").text().as_int();
			m_wpr_cfg.marker_frame_id = wpr.child("marker_frame_id").text().as_int();
			m_wpr_cfg.marker_record_frame_time = wpr.child("marker_record_frame_time").text().as_int();
			m_wpr_cfg.log_file_dir = wpr.child("log_file_dir").text().as_string();
		}
	}

	void dumpFileImpl(int index)
	{
		std::ofstream myfile;
		std::string file_name = m_wpr_cfg.log_file_dir +"/ProfileTest";
		file_name += std::to_string(index);
		file_name += ".log";
		myfile.open(file_name.c_str());
		for (auto& pair : m_profile_call_infos)
		{
			myfile << pair.first << "\t" << pair.second.time_cost << "\t" << pair.second.start_index << std::endl;
		}
		myfile.flush();
		myfile.close();
		m_profile_call_infos.clear();
	}

protected:
	CGameProfileSys()
	{
	}

	std::vector<std::pair<int, TimeInfo>> m_profile_call_infos;
	std::chrono::system_clock::time_point m_mark_last;

	struct wprCfg
	{
		bool open = false;
		int marker_min_interval = 2;
		int marker_frame_time = 100000;
		int marker_frame_id = -1;
		int marker_record_frame_time = 50;
		std::string start_cmd;
		std::string marker_cmd;
		std::string stop_cmd;
		std::string log_file_dir;
	};
	wprCfg m_wpr_cfg;

	int m_frame_call_times = 0;
	bool m_working = false;

};

extern "C" IGameProfileSys* GetProfileSys()
{
	return &CGameProfileSys::getInstance();
}

