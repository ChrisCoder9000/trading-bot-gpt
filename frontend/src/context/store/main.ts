import { analizeApi } from "@/services/api";
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: {
    [analizeApi.reducerPath]: analizeApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(analizeApi.middleware),
});

export default store;
export type RootState = ReturnType<typeof store.getState>;
