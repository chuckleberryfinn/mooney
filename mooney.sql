--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: _final_median(numeric[]); Type: FUNCTION; Schema: public; Owner: nemo
--

CREATE FUNCTION _final_median(numeric[]) RETURNS numeric
    LANGUAGE sql IMMUTABLE
    AS $_$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$_$;


ALTER FUNCTION public._final_median(numeric[]) OWNER TO nemo;

--
-- Name: median(numeric); Type: AGGREGATE; Schema: public; Owner: nemo
--

CREATE AGGREGATE median(numeric) (
    SFUNC = array_append,
    STYPE = numeric[],
    INITCOND = '{}',
    FINALFUNC = _final_median
);


ALTER AGGREGATE public.median(numeric) OWNER TO nemo;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: advice; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE advice (
    advice_id integer NOT NULL,
    response text NOT NULL
);


ALTER TABLE public.advice OWNER TO nemo;

--
-- Name: advice_advice_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE advice_advice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.advice_advice_id_seq OWNER TO nemo;

--
-- Name: advice_advice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE advice_advice_id_seq OWNED BY advice.advice_id;


--
-- Name: alerts; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE alerts (
    user_id integer NOT NULL,
    coin_id integer NOT NULL,
    euro numeric NOT NULL
);


ALTER TABLE public.alerts OWNER TO nemo;

--
-- Name: coins; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE coins (
    coin_id integer NOT NULL,
    name character varying(255) NOT NULL,
    ticker character varying(50) NOT NULL
);


ALTER TABLE public.coins OWNER TO nemo;

--
-- Name: coins_coin_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE coins_coin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.coins_coin_id_seq OWNER TO nemo;

--
-- Name: coins_coin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE coins_coin_id_seq OWNED BY coins.coin_id;


--
-- Name: daily_stats; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE daily_stats (
    coin_id integer NOT NULL,
    date date NOT NULL,
    average_euro numeric NOT NULL,
    max_euro numeric NOT NULL,
    min_euro numeric NOT NULL,
    std_dev numeric NOT NULL,
    median_euro numeric NOT NULL
);


ALTER TABLE public.daily_stats OWNER TO nemo;

--
-- Name: prices; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE prices (
    coin_id integer NOT NULL,
    "time" timestamp without time zone DEFAULT timezone('utc'::text, now()),
    euro numeric NOT NULL,
    dollar numeric NOT NULL
);


ALTER TABLE public.prices OWNER TO nemo;

--
-- Name: prices_archive; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE prices_archive (
    coin_id integer,
    "time" timestamp without time zone,
    euro numeric,
    dollar numeric
);


ALTER TABLE public.prices_archive OWNER TO nemo;

--
-- Name: remarks; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE remarks (
    remark_id integer NOT NULL,
    remark text NOT NULL
);


ALTER TABLE public.remarks OWNER TO nemo;

--
-- Name: remarks_remark_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE remarks_remark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.remarks_remark_id_seq OWNER TO nemo;

--
-- Name: remarks_remark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE remarks_remark_id_seq OWNED BY remarks.remark_id;


--
-- Name: replies; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE replies (
    reply_id integer NOT NULL,
    regex text NOT NULL
);


ALTER TABLE public.replies OWNER TO nemo;

--
-- Name: replies_remarks; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE replies_remarks (
    reply_id integer NOT NULL,
    remark_id integer NOT NULL
);


ALTER TABLE public.replies_remarks OWNER TO nemo;

--
-- Name: replies_reply_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE replies_reply_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.replies_reply_id_seq OWNER TO nemo;

--
-- Name: replies_reply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE replies_reply_id_seq OWNED BY replies.reply_id;


--
-- Name: user_replies; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE user_replies (
    user_id integer NOT NULL,
    reply_id integer NOT NULL
);


ALTER TABLE public.user_replies OWNER TO nemo;

--
-- Name: users; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(10) NOT NULL,
    administrator boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO nemo;

--
-- Name: users_remarks_replies; Type: TABLE; Schema: public; Owner: nemo; Tablespace: 
--

CREATE TABLE users_remarks_replies (
    user_id integer NOT NULL,
    remark_id integer NOT NULL,
    reply_id integer NOT NULL
);


ALTER TABLE public.users_remarks_replies OWNER TO nemo;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO nemo;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: weekly_stats; Type: VIEW; Schema: public; Owner: nemo
--

CREATE VIEW weekly_stats AS
 SELECT min(daily_stats.date) AS date,
    coins.name,
    max(daily_stats.max_euro) AS max,
    min(daily_stats.min_euro) AS min,
    avg(daily_stats.average_euro) AS avg,
    stddev(daily_stats.average_euro) AS stddev,
    median(daily_stats.median_euro) AS median
   FROM (daily_stats
     JOIN coins USING (coin_id))
  GROUP BY coins.name;


ALTER TABLE public.weekly_stats OWNER TO nemo;

--
-- Name: advice_id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY advice ALTER COLUMN advice_id SET DEFAULT nextval('advice_advice_id_seq'::regclass);


--
-- Name: coin_id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY coins ALTER COLUMN coin_id SET DEFAULT nextval('coins_coin_id_seq'::regclass);


--
-- Name: remark_id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY remarks ALTER COLUMN remark_id SET DEFAULT nextval('remarks_remark_id_seq'::regclass);


--
-- Name: reply_id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY replies ALTER COLUMN reply_id SET DEFAULT nextval('replies_reply_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: advice_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY advice
    ADD CONSTRAINT advice_pkey PRIMARY KEY (advice_id);


--
-- Name: advice_response_key; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY advice
    ADD CONSTRAINT advice_response_key UNIQUE (response);


--
-- Name: alerts_user_id_coin_id_euro_key; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_user_id_coin_id_euro_key UNIQUE (user_id, coin_id, euro);


--
-- Name: coins_name_key; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY coins
    ADD CONSTRAINT coins_name_key UNIQUE (name);


--
-- Name: coins_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY coins
    ADD CONSTRAINT coins_pkey PRIMARY KEY (coin_id);


--
-- Name: remarks_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY remarks
    ADD CONSTRAINT remarks_pkey PRIMARY KEY (remark_id);


--
-- Name: replies_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY replies
    ADD CONSTRAINT replies_pkey PRIMARY KEY (reply_id);


--
-- Name: replies_regex_key; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY replies
    ADD CONSTRAINT replies_regex_key UNIQUE (regex);


--
-- Name: replies_remarks_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY replies_remarks
    ADD CONSTRAINT replies_remarks_pkey PRIMARY KEY (reply_id, remark_id);


--
-- Name: unique_coin_date; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY daily_stats
    ADD CONSTRAINT unique_coin_date UNIQUE (coin_id, date);


--
-- Name: user_replies_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY user_replies
    ADD CONSTRAINT user_replies_pkey PRIMARY KEY (user_id, reply_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: nemo; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: prices_time_idx; Type: INDEX; Schema: public; Owner: nemo; Tablespace: 
--

CREATE INDEX prices_time_idx ON prices USING btree ("time");


--
-- Name: alerts_coin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_coin_id_fkey FOREIGN KEY (coin_id) REFERENCES coins(coin_id);


--
-- Name: alerts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: coin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT coin_id_fkey FOREIGN KEY (coin_id) REFERENCES coins(coin_id);


--
-- Name: daily_stats_coin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY daily_stats
    ADD CONSTRAINT daily_stats_coin_id_fkey FOREIGN KEY (coin_id) REFERENCES coins(coin_id);


--
-- Name: replies_remarks_remark_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY replies_remarks
    ADD CONSTRAINT replies_remarks_remark_id_fkey FOREIGN KEY (remark_id) REFERENCES remarks(remark_id);


--
-- Name: replies_remarks_reply_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY replies_remarks
    ADD CONSTRAINT replies_remarks_reply_id_fkey FOREIGN KEY (reply_id) REFERENCES replies(reply_id);


--
-- Name: user_replies_reply_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY user_replies
    ADD CONSTRAINT user_replies_reply_id_fkey FOREIGN KEY (reply_id) REFERENCES replies(reply_id);


--
-- Name: user_replies_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY user_replies
    ADD CONSTRAINT user_replies_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: users_remarks_replies_remark_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY users_remarks_replies
    ADD CONSTRAINT users_remarks_replies_remark_id_fkey FOREIGN KEY (remark_id) REFERENCES remarks(remark_id);


--
-- Name: users_remarks_replies_reply_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY users_remarks_replies
    ADD CONSTRAINT users_remarks_replies_reply_id_fkey FOREIGN KEY (reply_id) REFERENCES replies(reply_id);


--
-- Name: users_remarks_replies_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY users_remarks_replies
    ADD CONSTRAINT users_remarks_replies_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

