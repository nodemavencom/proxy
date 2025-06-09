/**
 * TypeScript definitions for NodeMaven JavaScript SDK
 */

export interface NodeMavenConfig {
  apiKey?: string;
  baseUrl?: string;
  proxyHost?: string;
  httpPort?: number;
  socks5Port?: number;
  timeout?: number;
}

export interface ProxyOptions {
  country?: string;
  region?: string;
  city?: string;
  isp?: string;
  zipCode?: string;
  connectionType?: string;
}

export interface ProxyConfig {
  host: string;
  http_port: number;
  socks5_port: number;
  username: string;
  password: string;
}

export interface UserInfo {
  username: string;
  proxy_username: string;
  proxy_password: string;
  traffic_used: number;
  traffic_limit: number;
  [key: string]: any;
}

export interface LocationQueryOptions {
  limit?: number;
  offset?: number;
  name?: string;
  code?: string;
  connectionType?: string;
}

export interface CountryQueryOptions extends LocationQueryOptions {}

export interface RegionQueryOptions extends LocationQueryOptions {
  countryCode?: string;
}

export interface CityQueryOptions extends LocationQueryOptions {
  countryCode?: string;
  regionCode?: string;
}

export interface IspQueryOptions extends LocationQueryOptions {
  countryCode?: string;
  regionCode?: string;
  cityCode?: string;
}

export interface StatisticsOptions {
  startDate?: string;
  endDate?: string;
  groupBy?: string;
}

export interface APIResponse<T = any> {
  results?: T[];
  count?: number;
  next?: string | null;
  previous?: string | null;
  [key: string]: any;
}

export class NodeMavenAPIError extends Error {
  statusCode: number | null;
  response: any;
  
  constructor(message: string, statusCode?: number | null, response?: any);
}

export class AuthenticationError extends NodeMavenAPIError {
  constructor(message: string, response?: any);
}

export class ValidationError extends NodeMavenAPIError {
  constructor(message: string, response?: any);
}

export class NotFoundError extends NodeMavenAPIError {
  constructor(message: string, response?: any);
}

export class RateLimitError extends NodeMavenAPIError {
  constructor(message: string, response?: any);
}

export class ServerError extends NodeMavenAPIError {
  constructor(message: string, statusCode?: number, response?: any);
}

export class NodeMavenClient {
  constructor(config?: NodeMavenConfig);
  
  getUserInfo(): Promise<UserInfo>;
  getCountries(options?: CountryQueryOptions): Promise<APIResponse>;
  getRegions(options?: RegionQueryOptions): Promise<APIResponse>;
  getCities(options?: CityQueryOptions): Promise<APIResponse>;
  getIsps(options?: IspQueryOptions): Promise<APIResponse>;
  getStatistics(options?: StatisticsOptions): Promise<APIResponse>;
  getProxyConfig(options?: ProxyOptions): Promise<ProxyConfig>;
  getSocks5ProxyUrl(options?: ProxyOptions): Promise<string>;
}

export {
  NodeMavenClient as default,
  NodeMavenClient,
  NodeMavenAPIError,
  AuthenticationError,
  ValidationError,
  NotFoundError,
  RateLimitError,
  ServerError
}; 