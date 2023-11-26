import { IAnalizeRequest, IAnalizeResponse } from "@/types/api/analize";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const analizeApi = createApi({
  reducerPath: "analizeApi",
  baseQuery: fetchBaseQuery({
    baseUrl:
      process.env.NODE_ENV === "production"
        ? "/api/analize"
        : "http://127.0.0.1:5000/api/analize",
  }),
  endpoints: (builder) => ({
    getAnalisis: builder.query<IAnalizeResponse, IAnalizeRequest>({
      query: ({ asset, lang }) => ({
        url: ``,
        method: "GET",
        params: { asset, lang },
      }),
    }),
  }),
});

export const { useLazyGetAnalisisQuery } = analizeApi;
