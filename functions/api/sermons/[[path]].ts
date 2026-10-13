import api from '../../../worker/index.ts';
export const onRequest: PagesFunction<Env> = context => api.fetch(context.request, context.env);
