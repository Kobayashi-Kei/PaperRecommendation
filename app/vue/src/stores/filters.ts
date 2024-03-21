import { defineStore } from 'pinia';
import axios from "axios";
import type { eventYearList } from '@/type';
import { settings } from "@/settings";

export const useFiltersStore = defineStore({
  id: 'filters',

  state: () => ({
    filterYear: "all",
    filterEvent: "all",
    eventYearList: {} as eventYearList,
  }),

  getters: {
    currentYearFilter(state): string {
      return state.filterYear;
    },

    currentEventFilter(state) {
      return state.filterEvent;
    },

    getEventYearList(state): eventYearList {
        return state.eventYearList;
    }
  },

  actions: {
    setYearFilter(year: string) {
      this.filterYear = year;
    },

    setEventFilter(event: string) {
      this.filterEvent = event;
    },

    setEventYears(eventYears: eventYearList) {
      this.eventYearList = eventYears;
    },

    getAllYearFromEventYears(eventYears: eventYearList): string[] {
      const years: string[] = [];
      for (let key in eventYears) {
        const eventYear = eventYears[key];
        for (let year of eventYear) {
          if (!years.includes(year)) {
            years.push(year);
          }
        }
      }
      years.sort().reverse();
      return years;
    },
    
    async getSearchCond() {
        const path = `http://${settings.ip_address}:${settings.port}/getSearchCond`;
        try {
          const response = await axios.post(path);
          const eventYears: eventYearList = { 'all': [] };
          for (let event in response.data) {
            // ex. ['all', '2021', '2020', ...]
            const tmpYears: string[] = ['all'].concat(response.data[event]);
            eventYears[event] = tmpYears;
          }
          const allYears = this.getAllYearFromEventYears(eventYears);
          eventYears['all'] = allYears;
          this.setEventYears(eventYears);
          /*
           * example of eventYears
           * {
           *   'all': ['all', 2023', '2022', ...],
           *   'acl': ['all', '2023', '2022', ...],
           *   'naccl': ['all', '2022', '2021', ...],
           * }
           */
        } catch (error) {
            console.log(error);
            console.log(path)
        }
    },
  }
});